import os

def save_html_file(html_code: str, filename: str = "index.html"):
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_code)

    print(f"Page saved to: {filepath}")
    return filepath