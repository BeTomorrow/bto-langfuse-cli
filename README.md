# bto-langfuse-cli

A set of CLI tools to interact with Langfuse, especially for prompt management.

## Installation

This project uses [uv](https://github.com/astral-sh/uv). You can install the project and its dependencies by running:

```bash
uv sync
```

Or you can install it using pip if you have the package:

```bash
pip install .
```

The CLI command is named `bto-langfuse-cli`.

## Configuration

The CLI uses environment variables for authentication with your Langfuse instance. You can create a `.env` file in the root directory or set these variables in your shell.

### `.env` Setup

Create a `.env` file with the following content:

```env
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com # Or your self-hosted URL
```

The CLI uses the standard `langfuse` Python SDK `get_client()` method, which automatically reads these environment variables.

## Usage

### Prompts Management

The `prompt` command group allows you to manage Langfuse prompts.

#### Promote Labels

The `promote` command allows you to copy a label from one version of all prompts to another. This is useful for moving prompts through different environments (e.g., from `dev` to `uat`).

**Command:**
```bash
bto-langfuse-cli prompt promote <src_label> <target_label> [--apply]
```

**Options:**
- `--apply`: Automatically apply the promotion without asking for confirmation.

**Examples:**

1. **Dry run / Confirmation mode:**
   ```bash
   bto-langfuse-cli prompt promote dev uat
   ```
   This will show a plan of which prompts will be updated (adding the `uat` label to all prompts that currently have the `dev` label) and ask for confirmation before applying.

2. **Auto-apply mode:**
   ```bash
   bto-langfuse-cli prompt promote dev uat --apply
   ```
   This will automatically update the labels for all prompts matching the source label.

#### Pull Prompts

The `pull` command downloads prompts from Langfuse to your local filesystem based on a specific label.

**Command:**
```bash
bto-langfuse-cli prompt pull <label> [type] [OPTIONS]
```

**Arguments:**
- `<label>`: The label to pull prompts from (e.g., `production`, `dev`). **(Required)**
- `[type]`: The type of prompt to pull. Can be `text` or `chat`. If not specified, both types are pulled.

**Options:**
- `-o, --output-dir <DIRECTORY>`: Directory to save the prompt files to. Defaults to `data/prompts`.
- `-f, --format <FORMAT>`: The output format. Currently only supports `md` (Markdown with YAML frontmatter). Defaults to `md`.

**Output Format (`md`):**
- **Text Prompts**: Saved as `.md` files containing a YAML frontmatter (with metadata like name, version, tags, labels, and last updated date) followed by the raw text prompt.
- **Chat Prompts**: Saved as `.md` files containing the same YAML frontmatter, followed by the chat messages serialized using XML-like tags (e.g., `<system>`, `<user>`).

**Examples:**

1. **Pull all prompts with a specific label:**
   ```bash
   bto-langfuse-cli prompt pull production
   ```

2. **Pull only chat prompts to a custom directory:**
   ```bash
   bto-langfuse-cli prompt pull dev chat -o ./my-local-prompts
   ```

## Development

To run the CLI during development:

```bash
uv run bto-langfuse-cli --help
```
