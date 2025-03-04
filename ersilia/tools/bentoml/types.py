import io
import os
import urllib
import uuid
from dataclasses import dataclass, field
from typing import (
    Any,
    BinaryIO,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

from bentoml import config
from multidict import CIMultiDict
from werkzeug.formparser import parse_form_data
from werkzeug.http import parse_options_header

from .utils.dataclasses import json_serializer

BATCH_HEADER = config("apiserver").get("batch_request_header")

# For non latin1 characters: https://tools.ietf.org/html/rfc8187
# Also https://github.com/benoitc/gunicorn/issues/1778
HEADER_CHARSET = "latin1"

JSON_CHARSET = "utf-8"


@json_serializer(fields=["uri", "name"], compat=True)
@dataclass(frozen=False)
class FileLike:
    """
    An universal lazy-loading wrapper for file-like objects.
    It accepts URI, file path or bytes and provides interface like opened file object.

    Attributes
    ----------
    bytes : bytes, optional

    uri : str, optional
        The set of possible uris is:

        - ``file:///home/user/input.json``
        - ``http://site.com/input.csv`` (Not implemented)
        - ``https://site.com/input.csv`` (Not implemented)

    name : str, default None
    """

    bytes_: Optional[bytes] = None
    uri: Optional[str] = None
    name: Optional[str] = None

    _stream: Optional[BinaryIO] = None

    def __post_init__(self):
        if self.name is None:
            if self._stream is not None:
                self.name = getattr(self._stream, "name", None)
            elif self.uri is not None:
                p = urllib.parse.urlparse(self.uri)
                if p.scheme and p.scheme != "file":
                    raise NotImplementedError(
                        f"{self.__class__} now supports scheme 'file://' only"
                    )
                _, self.name = os.path.split(self.path)

    @property
    def path(self):
        r"""
        supports:

        /home/user/file
        C:\Python27\Scripts\pip.exe
        \\localhost\c$\WINDOWS\clock.avi
        \\networkstorage\homes\user

        https://stackoverflow.com/a/61922504/3089381
        """
        parsed = urllib.parse.urlparse(self.uri)
        raw_path = urllib.request.url2pathname(urllib.parse.unquote(parsed.path))
        host = "{0}{0}{mnt}{0}".format(os.path.sep, mnt=parsed.netloc)
        path = os.path.abspath(os.path.join(host, raw_path))
        return path

    @property
    def stream(self):
        """
        Get the stream.

        Returns
        -------
        object
            The stream object.
        """
        if self._stream is not None:
            pass
        elif self.bytes_ is not None:
            self._stream = io.BytesIO(self.bytes_)
        elif self.uri is not None:
            self._stream = open(self.path, "rb")
        else:
            return io.BytesIO()
        return self._stream

    def read(self, size=-1):
        """
        Read from the stream.

        Parameters
        ----------
        size : int, optional
            The number of bytes to read. Default is -1 (read all).

        Returns
        -------
        bytes
            The read bytes.
        """
        # TODO: also write to log
        return self.stream.read(size)

    def seek(self, pos):
        """
        Seek to a position in the stream.

        Parameters
        ----------
        pos : int
            The position to seek to.

        Returns
        -------
        int
            The new position.
        """
        return self.stream.seek(pos)

    def tell(self):
        """
        Tell the current position in the stream.

        Returns
        -------
        int
            The current position.
        """
        return self.stream.tell()

    def close(self):
        """
        Close the stream.
        """
        if self._stream is not None:
            self._stream.close()

    def __del__(self):
        if self._stream and not self._stream.closed:
            self._stream.close()


class HTTPHeaders(CIMultiDict):
    """
    A case insensitive mapping of HTTP headers' keys and values.
    It also parses several commonly used fields for easier access.

    Attributes
    ----------
    content_type : str
        The value of ``Content-Type``, for example:
        - ``application/json``
        - ``text/plain``
        - ``text/csv``

    charset : str
        The charset option of ``Content-Type``

    content_encoding : str
        The charset option of ``Content-Encoding``

    Methods
    -------
    from_dict : create a HTTPHeaders object from a dict

    from_sequence : create a HTTPHeaders object from a list/tuple
    """

    @property
    def content_type(self) -> str:
        """
        Get the content type.

        Returns
        -------
        str
            The content type.
        """
        return parse_options_header(self.get("content-type"))[0].lower()

    @property
    def charset(self) -> Optional[str]:
        """
        Get the charset.

        Returns
        -------
        Optional[str]
            The charset, if available.
        """
        return parse_options_header(self.get("content-type"))[1].get("charset", None)

    @property
    def content_encoding(self) -> str:
        """
        Get the content encoding.

        Returns
        -------
        str
            The content encoding.
        """
        return parse_options_header(self.get("content-encoding"))[0].lower()

    @property
    def is_batch_input(self) -> bool:
        """
        Check if the input is batch input.

        Returns
        -------
        bool
            True if the input is batch input, False otherwise.
        """
        hv = parse_options_header(self.get(BATCH_HEADER))[0].lower()
        return hv == "true" if hv else None

    @classmethod
    def from_dict(cls, d: Mapping[str, str]):
        """
        Create an instance from a dictionary.

        Parameters
        ----------
        d : Mapping[str, str]
            The dictionary to create the instance from.

        Returns
        -------
        object
            The created instance.
        """
        return cls(d)

    @classmethod
    def from_sequence(cls, seq: Sequence[Tuple[str, str]]):
        """
        Create an instance from a sequence.

        Parameters
        ----------
        seq : Sequence[Tuple[str, str]]
            The sequence to create the instance from.

        Returns
        -------
        object
            The created instance.
        """
        return cls(seq)

    def to_json(self):
        """
        Convert the instance to JSON.

        Returns
        -------
        tuple
            The JSON representation of the instance.
        """
        return tuple(self.items())


@dataclass
class HTTPRequest:
    """
    A common HTTP Request object.
    It also parses several commonly used fields for easier access.

    Attributes
    ----------
    headers : HTTPHeaders

    body : bytes
    """

    headers: HTTPHeaders = HTTPHeaders()
    body: bytes = b""

    def __post_init__(self):
        if self.headers is None:
            self.headers = HTTPHeaders()
        elif isinstance(self.headers, dict):
            self.headers = HTTPHeaders.from_dict(self.headers)
        elif isinstance(self.headers, (tuple, list)):
            self.headers = HTTPHeaders.from_sequence(self.headers)

    @classmethod
    def parse_form_data(cls, self):
        """
        Parse form data.

        Parameters
        ----------
        self : object
            The object containing the form data.

        Returns
        -------
        tuple
            The parsed form data.
        """
        if not self.body:
            return None, None, {}
        environ = {
            "wsgi.input": io.BytesIO(self.body),
            "CONTENT_LENGTH": len(self.body),
            "CONTENT_TYPE": self.headers.get("content-type", ""),
            "REQUEST_METHOD": "POST",
        }
        stream, form, files = parse_form_data(environ, silent=False)
        wrapped_files = {
            k: FileLike(_stream=f, name=f.filename) for k, f in files.items()
        }
        return stream, form, wrapped_files

    @classmethod
    def from_flask_request(cls, request):
        """
        Create an instance from a Flask request.

        Parameters
        ----------
        request : object
            The Flask request object.

        Returns
        -------
        object
            The created instance.
        """
        return cls(
            tuple((k, v) for k, v in request.headers.items()),
            request.get_data(),
        )

    def to_flask_request(self):
        """
        Convert the instance to a Flask request.

        Returns
        -------
        object
            The Flask request object.
        """
        from werkzeug.wrappers import Request

        return Request.from_values(
            input_stream=io.BytesIO(self.body),
            content_length=len(self.body),
            headers=self.headers,
        )


@dataclass
class HTTPResponse:
    """
    Class representing an HTTP response.
    """

    status: int = 200
    headers: HTTPHeaders = HTTPHeaders()
    body: bytes = b""

    def __post_init__(self):
        if self.headers is None:
            self.headers = HTTPHeaders()
        elif isinstance(self.headers, dict):
            self.headers = HTTPHeaders.from_dict(self.headers)
        elif isinstance(self.headers, (tuple, list)):
            self.headers = HTTPHeaders.from_sequence(self.headers)

    def to_flask_response(self):
        """
        Convert the instance to a Flask response.

        Returns
        -------
        object
            The Flask response object.
        """
        import flask

        return flask.Response(
            status=self.status, headers=self.headers.items(), response=self.body
        )


# https://tools.ietf.org/html/rfc7159#section-3
JsonSerializable = Union[bool, None, Dict, List, int, float, str]

# https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
AwsLambdaEvent = Union[Dict, List, str, int, float, None]

Input = TypeVar("Input")
Output = TypeVar("Output")

ApiFuncArgs = TypeVar("ApiFuncArgs")
BatchApiFuncArgs = TypeVar("BatchApiFuncArgs")
ApiFuncReturnValue = TypeVar("ApiFuncReturnValue")
BatchApiFuncReturnValue = TypeVar("BatchApiFuncReturnValue")


@json_serializer(compat=True)
@dataclass
class InferenceResult(Generic[Output]):
    """
    The data structure that returned by BentoML API server.
    Contains result data and context like HTTP headers.
    """

    version: int = 0

    # payload
    data: Output = None
    err_msg: str = ""

    # meta
    task_id: Optional[str] = None

    # context
    http_status: Optional[int] = None
    http_headers: HTTPHeaders = HTTPHeaders()
    aws_lambda_event: Optional[dict] = None
    cli_status: Optional[int] = 0

    def __post_init__(self):
        if self.http_headers is None:
            self.http_headers = HTTPHeaders()
        elif isinstance(self.http_headers, dict):
            self.http_headers = HTTPHeaders.from_dict(self.http_headers)
        elif isinstance(self.http_headers, (tuple, list)):
            self.http_headers = HTTPHeaders.from_sequence(self.http_headers)

    @classmethod
    def complete_discarded(
        cls,
        tasks: Iterable["InferenceTask"],
        results: Iterable["InferenceResult"],
    ) -> Iterator["InferenceResult"]:
        """
        Generate InferenceResults based on successful inference results and
        fallback results of discarded tasks.
        """
        iterable_results = iter(results)
        try:
            for task in tasks:
                if task.is_discarded:
                    yield task.error
                else:
                    yield next(iterable_results)
        except StopIteration:
            raise StopIteration(
                "The results does not match the number of tasks"
            ) from None


@json_serializer(compat=True)
@dataclass
class InferenceError(InferenceResult):
    """
    The default InferenceResult when errors happened.
    """

    # context
    http_status: int = 500
    cli_status: int = 1


@json_serializer(compat=True)
@dataclass
class InferenceTask(Generic[Input]):
    """
    The data structure passed to the BentoML API server for inferring.
    Contains payload data and context like HTTP headers or CLI args.
    """

    version: int = 0

    # payload
    data: Input = None
    error: Optional[InferenceResult] = None

    # meta
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_discarded: bool = False
    batch: Optional[int] = None

    # context
    http_method: Optional[str] = None
    http_headers: HTTPHeaders = HTTPHeaders()
    aws_lambda_event: Optional[dict] = None
    cli_args: Optional[Sequence[str]] = None
    inference_job_args: Optional[Mapping[str, Any]] = None

    def discard(self, err_msg="", **context):
        """
        Discard this task. All subsequent steps will be skipped.

        Parameters
        ----------
        err_msg: str
            The reason why this task got discarded. It would be the body of
            HTTP Response, a field in AWS lambda event or CLI stderr message.

        *other contexts
            Other contexts of the fallback ``InferenceResult``
        """
        self.is_discarded = True
        self.error = InferenceError(err_msg=err_msg, **context)
        return self
