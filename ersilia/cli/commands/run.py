import json
import types

import click

from ... import ErsiliaModel
from ...core.session import Session
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

        # Process and display the results
        def display_result(res):
            if isinstance(res, list) and len(res) > 10:
                # Truncate long lists for clarity
                echo(json.dumps(res[:10], indent=4) + "\n... (truncated)", fg="yellow")
            else:
                echo(json.dumps(res, indent=4))

        if isinstance(result, types.GeneratorType):
            for res in result:
                if res is not None:
                    if as_table:
                        print_result_table(res)
                    else:
                        display_result(res)
                else:
                    echo("Something went wrong", fg="red")
        else:
            if as_table:
                print_result_table(result)
            else:
                try:
                    display_result(result)
                except Exception as e:
                    echo(f"An error occurred while displaying the result: {str(e)}", fg="red")

    return run
