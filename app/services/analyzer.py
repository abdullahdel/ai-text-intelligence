from dotenv import load_dotenv
import os
from pathlib import Path
from openai import OpenAI
from app.utils.logger import logger

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)

def analyze_text(text: str):

    if not text.strip():
        logger.error("Analyze request failed: empty text")
        return {"error": "Text darf nicht leer sein."}

    try:

        logger.info("Starting text analysis")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein Textanalyse-Assistent."},
                {"role": "user", "content": f"Analysiere folgenden Text:\n\n{text}"}
            ]
        )

        ai_answer = response.choices[0].message.content

        logger.info("Text analysis completed")

        return {
            "analysis": ai_answer
        }

    except Exception as e:

        logger.exception("OpenAI request failed")

        return {"error": str(e)}


def answer_question_with_context(question: str, context: str):
    if not question.strip():
        logger.error("Question answering failed: empty question")
        return {"error": "Frage darf nicht leer sein."}

    if not context.strip():
        logger.error("Question answering failed: empty context")
        return {"error": "Kontext darf nicht leer sein."}

    try:
        logger.info("Starting question answering with document context")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du bist ein Assistent für dokumentbezogene Fragen. "
                        "Beantworte die Frage nur auf Basis des gegebenen Kontexts. "
                        "Wenn die Antwort nicht im Kontext enthalten ist, sage das klar."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Kontext:\n\n{context}\n\nFrage:\n\n{question}",
                },
            ],
        )
        ai_answer = response.choices[0].message.content

        logger.info("Question answering completed")

        return {"answer": ai_answer}

    except Exception as e:
        logger.exception("OpenAI question answering request failed")
        return {"error": str(e)}