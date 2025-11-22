from google.genai import types
import pathlib

import os
import dotenv

from .config.config_gemini import client

dotenv.load_dotenv()

MODEL = os.getenv("MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = ""
with open("./app/services/llm/src/prompts/SYSTEMPROMPT.md", "r") as f:
    SYSTEM_PROMPT = f.read()


def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text  # type: ignore


def ask_gemini_system(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=prompt,
    )
    return response.text  # type: ignore


def parse_nl_code(prompt: str) -> str:
    # Retrieve and encode the PDF byte
    file_path = pathlib.Path("./app/services/llm/src/prompts/Proyecto_Gramatica.pdf")
    # Upload the PDF using the File API
    sample_file = client.files.upload(
        file=file_path,
    )
    response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=[
            "Considere la sintaxe de un pseudocodigo que se presenta en el pdf",
            sample_file,
            prompt,
        ],
    )
    return response.text  # type: ignore


def analisys_code(prompt: str, code: str) -> str:
    response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=[code, prompt],
    )
    return response.text  # type: ignore
