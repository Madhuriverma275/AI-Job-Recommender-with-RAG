import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()


def generate_career_advice(skills):
    if not skills:
        return "Please upload a resume with detectable skills to receive career advice."

    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not api_key:
        return "❌ HUGGINGFACEHUB_API_TOKEN not found. Add it to a .env file."

    prompt = (
        "You are a career coach. Suggest relevant career advice for someone with these skills: "
        f"{', '.join(skills)}."
    )

    try:
        llm = HuggingFaceEndpoint(
            repo_id="google/flan-t5-base",
            temperature=0.5,
            huggingfacehub_api_token=api_key,
        )
        return llm.invoke(prompt).strip()
    except Exception as exc:
        return f"❌ Career advice generation failed: {exc}"
