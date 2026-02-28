from __future__ import annotations
import typer
from importlib import metadata
from langfuse_cli.commands import prompt as prompt_commands

app = typer.Typer(name="langfuse-cli", help="Several tools to use Langfuse from terminal.")
app.add_typer(prompt_commands.prompt_app, name="prompt")

def version_callback(value: bool):
    if value:
        version = metadata.version("langfuse-cli")
        typer.echo(f"langfuse-cli version: {version}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Display the version and exit.",
    ),
):
    pass

if __name__ == "__main__":
    app()
