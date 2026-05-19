"""Commands for prompts management."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal

import typer

from bto_langfuse_cli.langfuse.langfuse_service import LangfuseService
from bto_langfuse_cli.langfuse.print_plan import print_plan
from bto_langfuse_cli.langfuse.prompt_exporter import MarkdownPromptExporter

prompt_app = typer.Typer(help="Manage Langfuse prompts.")


@prompt_app.command("promote")
def prompt_promote(
    args: Annotated[
        tuple[str, str],
        typer.Argument(help="src_label target_label)."),
    ],
    apply: Annotated[bool, typer.Option(help="Apply the promotion automatically")] = False,
) -> None:
    """Promote a label to another label.

    Examples:
      bto_langfuse-cli prompt promote dev uat → add uat label to all prompts with dev label. Ask before applying.
      bto_langfuse-cli prompt promote dev uat --apply → auto apply
    """
    langfuse = LangfuseService()
    from_label, to_label = args
    plan = langfuse.plan(from_label, to_label)
    print_plan(plan)
    if plan.has_changes():
        if apply or typer.confirm(f"Apply plan ?"):
            langfuse.apply(plan, to_label)


@prompt_app.command("pull")
def prompt_pull(
    label: Annotated[
        str,
        typer.Argument(help="The label to pull prompt from."),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory to save the prompts to.",
            dir_okay=True,
            file_okay=False,
        ),
    ] = Path("data/prompts"),
    prompt_type: Annotated[
        Literal["text", "chat"] | None,
        typer.Option(
            "--type", "-t", help="The type of prompt to pull or all if not specified."
        ),
    ] = None,
    prompt_format: Annotated[
        Literal["md"], typer.Option("--format", "-f", help="The output format.")
    ] = "md",
) -> None:
    """
    Pull prompt to filesystem from a given label and prompt type.

    Examples:
      bto_langfuse-cli prompt pull dev -o data/prompts -t chat -- → pull all chat prompts tagged dev to data/prompts.
    """
    langfuse = LangfuseService()
    output_dir.mkdir(parents=True, exist_ok=True)

    if prompt_format == "md":
        exporter = MarkdownPromptExporter()
    else:
        typer.echo(f"Unsupported format: {prompt_format}", err=True)
        raise typer.Exit(code=1)

    written = 0
    skipped = 0

    typer.echo(f"Pulling prompts with label '{label}'...")

    for meta, prompt_client in langfuse.get_prompts_with_meta(
        label=label, prompt_type=prompt_type
    ):
        try:
            out_path = exporter.export(meta, prompt_client, output_dir)
            if out_path:
                typer.echo(f"Wrote {out_path}")
                written += 1
        except Exception as e:
            typer.echo(f"Error exporting {meta.name}: {e}", err=True)
            skipped += 1

    typer.echo(f"Done. Pulled {written} prompts to {output_dir} (Skipped: {skipped})")
