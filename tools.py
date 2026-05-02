from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def create_file(filename="file.txt"):
    path = OUTPUT_DIR / filename
    path.write_text("")
    return f"File '{filename}' created successfully."


def write_code(filename="code.py", code="print('Hello World')"):
    path = OUTPUT_DIR / filename
    path.write_text(code)
    return f"Code written to '{filename}'."


def summarize(text):
    return text[:100] + "..."
