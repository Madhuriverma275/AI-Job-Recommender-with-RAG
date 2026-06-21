import ast
from PyPDF2 import PdfReader

KNOWN_SKILLS = [
    "python",
    "java",
    "javascript",
    "machine learning",
    "data science",
    "sql",
    "react",
    "node",
    "aws",
    "docker",
    "kubernetes",
]

def clean_skills(skill_text):
    if not isinstance(skill_text, str):
        return ""

    try:
        skills = ast.literal_eval(skill_text)
        if isinstance(skills, (list, tuple)):
            return " ".join(str(skill).strip() for skill in skills if skill)
        return str(skills).strip()
    except (ValueError, SyntaxError):
        return skill_text.strip()


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    pages = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages.append(page_text)
    return "\n".join(pages)


def extract_skills(text):
    text = (text or "").lower()
    return [skill for skill in KNOWN_SKILLS if skill in text]