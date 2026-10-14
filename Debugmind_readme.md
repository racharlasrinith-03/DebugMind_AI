# DebugMind AI

**An AI-powered self-correcting Python code assistant**

DebugMind AI generates Python code from natural-language tasks, executes the generated program, detects errors, and attempts to correct the code automatically using Groq and LangChain.

> **Tagline:** Generate. Debug. Correct. Execute.

## Features

- **AI Code Generation:** Create Python programs from plain-English instructions.
- **Automatic Execution:** Run generated code using the current Python interpreter.
- **Error Detection:** Capture syntax errors, runtime errors, and execution timeouts.
- **Self-Correction:** Send error details to the LLM and request corrected code.
- **Retry Mechanism:** Attempt corrections up to a configurable maximum number of times.
- **Simple CLI:** Enter a coding task directly in the terminal.

## Technology Stack

- Python
- Groq API
- LangChain
- `langchain-groq`
- `python-dotenv`
- Python `subprocess` and `ast` modules

## Project Structure

```text
debugmind-ai/
├── agent.py
├── executor.py
├── prompts.py
├── .env
├── .gitignore
├── requirements.txt
└── generated_code.py   # Created when the agent runs
```

## Prerequisites

- Python 3.10 or a compatible version supported by your installed dependencies
- A Groq API key
- Internet access for LLM requests

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/debugmind-ai.git
cd debugmind-ai
```

Replace `YOUR_USERNAME` with your GitHub username and use your actual repository URL.

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Create a `requirements.txt` file containing:

```text
langchain-groq
python-dotenv
```

Then run:

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own key. **Never commit your real API key to GitHub.**

## Run the Project

Start the assistant:

```bash
python agent.py
```

Enter a task when prompted. For example:

```text
Build a student management system using Python and SQLite with add, update,
delete, search, and list operations. Include input validation and error handling.
```

DebugMind AI generates the code, saves it to `generated_code.py`, executes it, and attempts to fix detected errors when necessary.

## Configuration

The current implementation uses the following setting in `agent.py`:

```python
MAX_RETRIES = 5
```

The execution timeout is configured in `executor.py` (for example, 60 seconds). Adjust these values according to your needs. Increasing the timeout does not fix infinite loops or inefficient algorithms.

## How It Works

1. **Receive task:** Read the coding request from the terminal.
2. **Generate code:** Ask the Groq-powered language model to produce Python code.
3. **Save code:** Write the generated source to `generated_code.py`.
4. **Validate and execute:** Check Python syntax and run the program with a timeout.
5. **Inspect failures:** Capture error messages or timeout details.
6. **Correct code:** Send the task, current code, and error details back to the model.
7. **Retry:** Repeat until execution succeeds or the retry limit is reached.

## Important Notes

- Successful execution does not guarantee that the generated program is logically correct. Add automated tests for important tasks.
- Complex programs may require additional dependencies, files, configuration, or user-specific data.
- Generated code is executed on your machine. Run it only in a controlled environment and avoid giving it unrestricted access to sensitive files, credentials, or network resources.
- The assistant can still fail if the model produces incorrect code, the API is unavailable, a dependency is missing, or the task requires unsupported external resources.

## `.gitignore`

Consider creating a `.gitignore` file with:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
generated_code.py
```

Only ignore `generated_code.py` if you do not want generated examples committed to the repository.

## Future Improvements

- Add automated unit tests and expected-output checks.
- Support multi-file Python projects.
- Add dependency detection and clearer installation guidance.
- Add execution sandboxing and resource limits.
- Add a Streamlit interface and execution history.
- Support additional languages and structured debugging reports.

## Contributing

Contributions, suggestions, and bug reports are welcome. Open an issue to discuss a proposed improvement before submitting a pull request.

## License

Choose a license for your repository (for example, MIT) and add the corresponding `LICENSE` file before distributing the project.

---

**DebugMind AI — Generate. Debug. Correct. Execute.**
