## Project Overview

**`main.py`** is a small Python script that demonstrates **prompt engineering** and **LLM integration** through several independent tasks: support-ticket classification, logic-puzzle solving, Python code generation from natural language, and email signature parsing. It uses the **Chat Completions** interface to send structured prompts and read model replies as plain text (often JSON-shaped).

**Purpose**

- Centralize experiments and assignment-style functions that call a hosted language model with task-specific prompts.
- Show a single shared helper (`get_completion`) used by all higher-level functions.

**Problem / use case**

- Automate or assist **support triage** (category + priority).
- Solve **constraint-based ordering puzzles** with guided reasoning instructions.
- **Generate Python functions** from descriptions.
- **Extract contact fields** (name, email, phone) from unstructured email bodies.

---

## Implementation Details

### Workflow

1. **Environment** — On startup, `load_dotenv()` loads variables from `.env`. An `AzureOpenAI` client is created with `API_KEY`, `AZURE_ENDPOINT`, and a fixed `API_VERSION` (`2024-02-01`).
2. **Shared API call** — `get_completion(messages, model=...)` calls `client.chat.completions.create` and returns `response.choices[0].message.content` as a string. Errors are caught and returned as a string starting with `"An error occurred:"`.
3. **Demo execution** — The script runs a **technical debt** one-shot completion, then several **`classify_and_prioritize`** calls, a **`solve_logic_puzzle`** example, **`python_function_generator`** examples, and **`parse_email_body`** on a sample email. Running the file therefore issues multiple API calls in sequence.

### Design decisions

- **One client, many prompts** — All tasks reuse `get_completion` instead of duplicating HTTP/client logic.
- **Prompt-in-function** — Each task builds its own system/user-style prompt as an f-string, keeping behavior local and easy to edit.
- **String outputs** — Return values are raw model text; callers are expected to parse JSON separately if strict structure is required (except where prompts request JSON).
- **Azure OpenAI SDK** — The project uses `AzureOpenAI` from the official `openai` package, configured for an Azure-compatible endpoint rather than calling `api.openai.com` directly.

---

## Functions Documentation

| Function | Purpose | Parameters | Return value |
|----------|---------|------------|--------------|
| `get_completion` | Sends a chat completion request and returns the assistant’s reply text. | `messages` (list of dicts, e.g. `[{"role":"user","content":"..."}]`), `model` (optional; defaults to `DEPLOYMENT_NAME`, e.g. `gpt-4`). | `str` — assistant message content, or an error string on failure. |
| `classify_and_prioritize` | Classifies a support ticket and assigns priority via the model. | `ticket_text` (`str`) — free-text ticket. | `str` — model output intended as a single JSON object with `"category"` and `"priority"`. |
| `solve_logic_puzzle` | Solves a line-ordering style logic puzzle with structured instructions in the prompt. | `puzzle` (`str`) — puzzle description. | `str` — explanation plus solution (e.g. ordered list in text). |
| `python_function_generator` | Generates Python source for a function from a natural-language description. | `description` (`str`) — what the function should do. | `str` — model output (prompt asks for code between ` ```python ` markers). |
| `parse_email_body` | Extracts primary sender contact info from an email body. | `email_text` (`str`) — raw email body. | `str` — JSON-like text with `name`, `email`, `phone` (or `null` / `None` per prompt), or as the model interprets “no contact found”. |

---

## Solutions & Approach

| Task | How it is addressed | Assumptions / edge cases |
|------|---------------------|---------------------------|
| **Ticket classification** | Prompt fixes allowed categories and priorities and asks for **only** a JSON object with `"category"` and `"priority"`, discouraging markdown fences. | Model may still add formatting or wording; parsing is not enforced in code. |
| **Logic puzzle** | Prompt embeds an example puzzle + answer format, asks for short explanation and ordered list, and instructs internal reasoning without dumping every step. | Solution correctness depends on the model; ambiguous puzzles may yield wrong orders. |
| **Python generation** | Few-shot style example (`calculate_sum`) and instruction to wrap output in ` ```python ` blocks. | Generated code should be reviewed before execution; no sandbox in script. |
| **Email parsing** | Prompt asks for JSON with `name`, `email`, `phone`, `null` for missing fields, and `None` when no primary contact is found. | Forwarded threads and multiple signatures may confuse the model; output is still plain text. |

---

## Task Summary

- **Chat client setup** with Azure OpenAI–compatible configuration.
- **Demo** one-line explanation of “technical debt.”
- **Support tickets** — classify into Bug / Feature Request / Question / Praise / Complaint and assign High / Medium / Low.
- **Logic puzzle** — ordering with constraints (example: five people in a line).
- **Code generation** — Python functions from descriptions (e.g. average, percentage).
- **Email parsing** — extract sender name, email, and phone from a message body.

---

## Setup & Usage

### Prerequisites

- **Python** 3.9+ recommended (3.10+ typical for current `openai` releases).
- Network access to your **Azure OpenAI** (or compatible) endpoint.

### Dependencies

Install packages used by `main.py`:

```bash
pip install openai python-dotenv
```

### Environment variables

Create a `.env` file in the project root (do not commit secrets):

```env
API_KEY=your_api_key_here
AZURE_ENDPOINT=https://your-resource.openai.azure.com
```

`main.py` reads `API_KEY` and `AZURE_ENDPOINT` via `os.getenv`. `DEPLOYMENT_NAME` is set in code (default `gpt-4`); change it if your deployment name differs.

### Run

```bash
python main.py
```

**Note:** Running the script executes **all** embedded `print` demos (classification tests, puzzle, code generation, email parsing) and will consume API quota accordingly.


## OpenAI API Integration

This repository’s `main.py` uses the **`openai` Python library** with **`AzureOpenAI`** and the **Chat Completions** API shape (`client.chat.completions.create`, `messages`, `model` deployment name). That matches the same conceptual API described in OpenAI’s documentation (messages in, assistant message string out).

**Official resources**

- **Documentation:** [https://platform.openai.com/docs](https://platform.openai.com/docs) — guides for Chat Completions, authentication concepts, and SDK usage (also applicable when using OpenAI-compatible gateways).
- **Pricing:** [https://platform.openai.com/pricing](https://platform.openai.com/pricing) — list pricing for OpenAI-hosted models (your Azure or enterprise endpoint may bill differently).

**How to obtain an API key (OpenAI platform)**

1. Create or sign in to an account at [OpenAI](https://platform.openai.com/).
2. Open **API keys** in the dashboard and create a new secret key.
3. Store it securely (environment variable or secret manager); never commit it to git.

For **Azure OpenAI**, keys and endpoints are created in the **Azure Portal** for your resource; `main.py` expects `API_KEY` and `AZURE_ENDPOINT` accordingly.

**Usage in this project**

- `get_completion` builds the `messages` list and calls the chat completions endpoint once per invocation.
- Downstream functions only vary the **prompt text** and pass a single user message (or could be extended with system messages).

---

## Examples (optional)

Sample **inputs** (as in `main.py`):

- **Classification:** `"The app crashes every time I try to upload a video."`
- **Classification:** `"What are the steps to open a support ticket?"`
- **Puzzle:** Five friends Ethan, Farhan, Gaurav, Harsh, Imran with ordering constraints (see script).
- **Code gen:** *“Create a Python function named `calculate_average` that takes a list of numbers and returns their average.”*
- **Email:** A short message ending with `John Doe`, `john.doe@example.com`, `1234567890`.

**Outputs** are **model-dependent**. Typical shapes:

- Classification: `{"category": "Bug", "priority": "High"}` (as a single-line or pretty-printed string).
- Puzzle: A short explanation plus a line like `Solution: [...]`.
- Code: A `def` block inside markdown code fences.
- Email: JSON text with `name`, `email`, `phone`.

---
