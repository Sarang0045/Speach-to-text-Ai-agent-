import os

OUTPUT_DIR = "output"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def create_file(filename="file.txt"):
    """
    Creates an empty file inside output/
    """

    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w") as f:
        f.write("")

    return f"File '{filename}' created successfully."


def write_code(filename="code.py", code="print('Hello World')"):
    """
    Writes code into a file inside output/
    """

    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w") as f:
        f.write(code)

    return f"Code written to '{filename}'."


def summarize(text):
    """
    Simple summarization (we will improve later using LLM)
    """

    summary = text[:100] + "..."

    return summary