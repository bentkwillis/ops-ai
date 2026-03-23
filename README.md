# ops-ai

An interactive SSH troubleshooting assistant that uses an LLM to propose investigation commands step by step.

The tool opens a multiplexed SSH connection to a remote Linux host, asks an LLM for the best next command, and requires explicit user approval before every command is run.

## Features

- Uses an LLM to analyze incident context and suggest the next investigation step.
- Executes commands remotely over SSH using a persistent control socket.
- Keeps short command/output history to improve follow-up suggestions.
- Validates model output against a strict JSON schema.
- Detects potentially dangerous commands and asks for an extra override.
- Supports iterative investigation with periodic summary checkpoints.

## How It Works

1. Start the app with a target SSH host.
2. Enter a problem statement at the prompt.
3. The app asks the LLM for:
   - analysis
   - a 3-step plan
   - one next command
   - confidence and rationale
4. You can approve, edit, or reject the proposed command.
5. Command output is fed back into history for the next reasoning step.
6. The loop ends when the model reports `done=true` or you stop.

## Project Structure

- `main.py`: CLI entry point, SSH command execution loop, approvals, and summaries.
- `llm.py`: OpenAI client integration and prompt construction.
- `prompts.py`: System prompt for model behavior and response schema.
- `validation.py`: Response schema validation.
- `policy.py`: Dangerous command pattern checks.

## Requirements

- Python 3.9+
- SSH client available in your shell
- OpenAI API key

Python packages:

- `openai`
- `python-dotenv`

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install openai python-dotenv
```

3. Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run:

```bash
python main.py <host>
```

Example:

```bash
python main.py ubuntu@10.0.0.25
```

Then at the prompt, enter the issue you want to investigate, for example:

```text
nginx returns 502 on the API endpoint
```

For each proposed command, choose:

- `y` to run it
- `edit` to modify it
- `n` to stop

Type `exit` or `quit` to end the session.

## Safety Notes

- Commands are not auto-executed; every command requires confirmation.
- Commands matching dangerous patterns trigger an additional override prompt.
- The dangerous-pattern list is substring-based. Tune `policy.py` for your environment and risk tolerance.

## Current Limitations

- No retries/backoff around SSH command execution.
- Policy checks are broad and may block some legitimate commands.
- Conversation history resets for each new top-level user prompt.
- Uses a fixed model (`gpt-4o-mini`) in code.

## Development Ideas

- Make model, temperature, and max steps configurable.
- Add structured logging and transcript export.
- Add unit tests for validation and policy matching.
- Improve command safety policy with allowlists and command parsing.
