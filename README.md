# langfuse-cli

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

The CLI command is named `langfuse-cli`.

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
langfuse-cli prompt promote <src_label> <target_label> [--apply]
```

**Options:**
- `--apply`: Automatically apply the promotion without asking for confirmation.

**Examples:**

1. **Dry run / Confirmation mode:**
   ```bash
   langfuse-cli prompt promote dev uat
   ```
   This will show a plan of which prompts will be updated (adding the `uat` label to all prompts that currently have the `dev` label) and ask for confirmation before applying.

2. **Auto-apply mode:**
   ```bash
   langfuse-cli prompt promote dev uat --apply
   ```
   This will automatically update the labels for all prompts matching the source label.

## Development

To run the CLI during development:

```bash
uv run langfuse-cli --help
```
