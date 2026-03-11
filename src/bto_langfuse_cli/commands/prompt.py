"""Commands for prompts management."""

from __future__ import annotations

from typing import Annotated

import typer

from bto_langfuse_cli.langfuse.langfuse_service import LangfuseService, Plan
from bto_langfuse_cli.langfuse.print_plan import print_plan

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
      bto_langfuse-cli prompt promote dev uat                  → add uat label to all prompts with dev label. Ask before applying.
      bto_langfuse-cli prompt promote dev uat --apply          → auto apply
    """
    langfuse = LangfuseService()
    from_label, to_label = args
    plan = langfuse.plan(from_label, to_label)
    print_plan(plan)
    if plan.has_changes():
        if apply or typer.confirm(f"Apply plan ?"):
            langfuse.apply(plan, to_label)
