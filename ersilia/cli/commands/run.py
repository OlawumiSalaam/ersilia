import types

import click

from ... import ErsiliaModel
from ...core.session import Session
from ...io.shape import InputShapeSingle
from ...io.types.compound import IO
from ...utils.exceptions_utils.api_exceptions import UnprocessableInputError
from ...utils.terminal import print_result_table
from .. import echo
from . import ersilia_cli


def run_cmd():
    """
    Runs a specified model.

    This command allows users to run a specified model with given inputs.

    Returns
    -------
    function
        The run command function to be used by the CLI and for testing in the pytest.

    Examples
    --------
    .. code-block:: console

        Run a model by its ID with input data:
        $ ersilia run -i <input_data> --as-table

        Run a model with batch size:
        $ ersilia run -i <input_data> -b 50
    """

    # Example usage: ersilia run -i {INPUT} [-o {OUTPUT} -b {BATCH_SIZE}]
    @ersilia_cli.command(short_help="Run a served model", help="Run a served model")
    @click.option("-i", "--input", "input", required=True, type=click.STRING)
    @click.option(
        "-o", "--output", "output", required=False, default=None, type=click.STRING
    )
    @click.option(
        "-b", "--batch_size", "batch_size", required=False, default=100, type=click.INT
    )
    @click.option("--as_table/-t", is_flag=True, default=False)
    def run(input, output, batch_size, as_table):
        session = Session(config_json=None)
        model_id = session.current_model_id()
        service_class = session.current_service_class()
        track_runs = session.tracking_status()

        output_source = session.current_output_source()
        if model_id is None:
            echo(
                "No model seems to be served. Please run 'ersilia serve ...' before.",
                fg="red",
            )
            return

        mdl = ErsiliaModel(
            model_id,
            output_source=output_source,
            service_class=service_class,
            config_json=None,
            track_runs=track_runs,
        )
        try:
            # Early validation: if input is not a file, assume it's a SMILES string.
            import json

            try:
                # Attempt to parse the input as JSON.
                smiles_data = json.loads(input)
            except json.JSONDecodeError:
                # If parsing fails, assume it's a single SMILES string.
                smiles_data = input

            io_instance = IO(InputShapeSingle())

            # If the parsed data is a list, validate each SMILES string.
            if isinstance(smiles_data, list):
                for s in smiles_data:
                    if not io_instance.is_input(s):
                        raise UnprocessableInputError
            else:
                # Otherwise, treat it as a single SMILES string.
                if not io_instance.is_input(smiles_data):
                    raise UnprocessableInputError
        except ValueError as ve:
            raise UnprocessableInputError(str(ve))

        result = mdl.run(
            input=input,
            output=output,
            batch_size=batch_size,
            track_run=track_runs,
        )
        iter_values = []
        if isinstance(result, types.GeneratorType):
            for r in result:
                if r is not None:
                    iter_values.append(r)
            if as_table:
                print_result_table(iter_values)
            else:
                echo(json.dumps(iter_values, indent=4))
        else:
            if as_table:
                print_result_table(result)
            else:
                try:
                    echo(result)
                except Exception:
                    echo(
                        f"Error: Could not print the result for output given path: {result}."
                    )
        return

    return run
