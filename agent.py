
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from prompts import SYSTEM_PROMPT, DEBUG_PROMPT
from executor import run_code

load_dotenv()

MAX_RETRIES = 5
OUTPUT_FILE = Path("generated_code.py")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def clean_code(code):
    code = code.strip()

    if code.startswith("```"):
        lines = code.splitlines()[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        code = "\n".join(lines)

    return code.strip()


def generate_code(task):
    prompt = f"""
{SYSTEM_PROMPT}

USER TASK:
{task}

Write complete, executable Python code.
Handle edge cases and use efficient algorithms.
Do not use input() unless explicitly required.
Return only Python code without Markdown fences.
"""
    response = llm.invoke(prompt)
    return clean_code(response.content)


def fix_code(task, code, error):
    prompt = f"""
{DEBUG_PROMPT}

USER TASK:
{task}

CURRENT CODE:
{code}

ERROR OR TEST RESULT:
{error}

Find the actual cause and fix it.
Preserve all required features.
Check syntax, logic, edge cases and performance.
Return the complete corrected Python code only.
Do not use Markdown fences.
"""
    response = llm.invoke(prompt)
    return clean_code(response.content)


def main():
    task = input("\nEnter your coding task: ").strip()

    if not task:
        print("Please enter a valid coding task.")
        return

    try:
        code = generate_code(task)

        for attempt in range(1, MAX_RETRIES + 1):
            OUTPUT_FILE.write_text(code, encoding="utf-8")

            print(f"\nAttempt {attempt}/{MAX_RETRIES}: Running code...")

            success, result = run_code(
                str(OUTPUT_FILE),
                timeout=60
            )

            if success:
                print("\nCode executed successfully!")
                print("\n--- Generated Code ---\n")
                print(code)
                print("\n--- Program Output ---\n")
                print(result)
                return

            print("\nExecution failed:")
            print(result)

            if attempt < MAX_RETRIES:
                print("\nTrying to correct the code...")
                code = fix_code(task, code, result)

        print("\nAgent failed after maximum retries.")
        print(f"Check the generated code in: {OUTPUT_FILE.resolve()}")

    except Exception as error:
        print(f"\nAgent error: {error}")


if __name__ == "__main__":
    main()
