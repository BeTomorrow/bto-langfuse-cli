from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from langfuse.api import PromptType
from langfuse.api.prompts.types.prompt_meta import PromptMeta
from langfuse.model import TextPromptClient, ChatPromptClient


class PromptExporter(ABC):
    """Interface for prompt exporters."""

    @abstractmethod
    def export(
        self,
        meta: PromptMeta,
        prompt_client: TextPromptClient | ChatPromptClient,
        output_dir: Path,
    ) -> Path | None:
        """
        Export the prompt as a file to the given directory.

        Args:
            meta: The metadata of the prompt from the list API.
            prompt_client: The detailed prompt client object.
            output_dir: The directory where the prompt should be saved.

        Returns:
            The path to the generated file, or None if skipped.
        """
        pass


class MarkdownPromptExporter(PromptExporter):
    """
    Exports prompts to Markdown files with YAML frontmatter
    and XML section for Chat prompts.
    """

    def _yaml_quote(self, s: str) -> str:
        if s == "":
            return '""'
        if any(c in s for c in (":", "#", "\n", '"')) or s.strip() != s:
            escaped = s.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'
        return s

    def _format_yaml_block_list(self, key: str, items: list[str]) -> str:
        if not items:
            return f"{key}: []"
        lines = [f"{key}:"]
        for item in items:
            lines.append(f"  - {self._yaml_quote(item)}")
        return "\n".join(lines)

    def _metadata_header(
        self,
        name: str,
        version: int,
        prompt_type: str,
        labels: list[str],
        tags: list[str],
        last_updated_at: datetime,
    ) -> str:
        lines = [
            "---",
            f"name: {self._yaml_quote(name)}",
            f"version: {version}",
            f"type: {prompt_type}",
            self._format_yaml_block_list("labels", labels),
            self._format_yaml_block_list("tags", tags),
            f"last_updated_at: {self._yaml_quote(last_updated_at.isoformat())}",
            "---",
        ]
        return "\n".join(lines) + "\n"

    def _serialize_chat_prompt(self, client: ChatPromptClient) -> str:
        parts: list[str] = []
        for msg in client.prompt:
            if msg["type"] == "message":
                role = msg["role"]
                content = msg["content"]
                parts.append(f"<{role}>\n\n{content}\n\n</{role}>")
            elif msg["type"] == "placeholder":
                name = msg["name"]
                parts.append(f"<placeholder>{{{{{name}}}}}</placeholder>")
            else:
                raise ValueError(f"Unsupported chat message entry: {msg!r}")
        return "\n\n".join(parts)

    def export(
        self,
        meta: PromptMeta,
        prompt_client: TextPromptClient | ChatPromptClient,
        output_dir: Path,
    ) -> Path | None:
        out_path = Path(output_dir, meta.name).with_suffix(".md")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        langfuse_prompt_type = "text" if meta.type is PromptType.TEXT else "chat"

        header = self._metadata_header(
            name=prompt_client.name,
            version=prompt_client.version,
            prompt_type=langfuse_prompt_type,
            labels=list(prompt_client.labels),
            tags=list(prompt_client.tags),
            last_updated_at=meta.last_updated_at,
        )

        match prompt_client:
            case TextPromptClient():
                body = prompt_client.prompt
            case ChatPromptClient():
                body = self._serialize_chat_prompt(prompt_client)
            case _:
                raise ValueError(
                    f"Expected ChatPromptClient or TextPromptClient for {meta.name}"
                )

        combined = f"{header}\n{body}\n"
        out_path.write_text(combined, encoding="utf-8")
        return out_path
