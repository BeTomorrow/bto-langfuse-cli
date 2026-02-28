from __future__ import annotations
import typer
from langfuse_cli.commands import prompt as prompt_commands
app = typer.Typer(name="langfuse-cli", help="Several tools to use Langfuse from terminal.")
app.add_typer(prompt_commands.prompt_app, name="prompt")

if __name__ == "__main__":
    app()
