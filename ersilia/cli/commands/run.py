import json
import types

import click

from ... import ErsiliaModel
from ...core.session import Session
from ...utils.terminal import print_result_table
from .. import echo
from . import ersilia_cli


def truncate_output(output, max_items=10, max_chars=500):
    """
    Truncates long outputs for better readability.

    Parameters
    ----------
    output : Any
        The output to process and truncate.
    max_items : int, optional
        Maximum number of items to display for arrays/lists or dictionary keys.
    max_chars : int, optional
        Maximum number of characters to display for strings.

    Returns
    -------
    str
        The truncated output as a formatted string.
    """
    if isinstance(output, list):
        if len(output) > max_items:
            return f"{output[:max_items]} ... (and {len(output) - max_items} more items)"
        return str(output)
    elif isinstance(output, dict):
        formatted = json.dumps(output, indent=4)
        lines = formatted.splitlines()
        if len(lines) > max_items:
            return "\n".join(lines[:max_items]) + f"\n... (and {len(lines) - max_items} more lines)"
        return formatted
    elif isinstance(output, str):
        if len(output) > max_chars:
            return f"{output[:max_chars]}... (truncated)"
        return output
    else:
        return str(output)


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
    @click.option("--as-table/-t", is_flag=True, default=False)
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
        result = mdl.run(
            input=input,
            output=output,
            batch_size=batch_size,
            track_run=track_runs,
        )

        if isinstance(result, types.GeneratorType):
            for result in mdl.run(input=input, output=output, batch_size=batch_size):
                if result is not None:
                    truncated = truncate_output(result)  # Truncate the output
                    if as_table:
                        print_result_table(truncated)  # Print truncated result as table
                    else:
                        echo(truncated)  # Print truncated raw output
                else:
                    echo("Something went wrong", fg="red")  # Print error if result is None
        else:
            # Allow user to print full result as a table
            if as_table:
                if isinstance(result, dict):
                    # Print full result as table if available
                    print_result_table(result)  
                else:
                    echo("Result cannot be displayed as a table", fg="red")
            else:
                try:
                    truncated = truncate_output(result)  # Truncate only for terminal output
                    echo(truncated)  # Print truncated result
                except Exception as e:
                    echo(f"Error: {e}", fg="red")  # Print error if echo fails
                    print_result_table(result)  # Fallback: Print full result as a table


    return run
