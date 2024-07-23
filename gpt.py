from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def get_gpt_response(data: str, instructions: list):
    # Ensure unique titles in a case-insensitive manner
    seen_titles = set()
    unique_instructions = []
    for instruction in instructions:
        title = instruction["title"].strip().lower().replace(" ", "_")
        if title not in seen_titles:
            seen_titles.add(title)
            unique_instructions.append(
                {
                    "title": title,
                    "data_type": instruction["data_type"],
                    "description": instruction["description"],
                }
            )

    function_properties = {}
    for instruction in unique_instructions:
        title = instruction["title"]
        function_properties[title] = {
            "type": instruction["data_type"],
            "description": instruction["description"],
        }

    function_descriptions = [
        {
            "name": "extract_data",
            "description": "Extract information from file. Return 'not found' if field is not found.",
            "parameters": {
                "type": "object",
                "properties": function_properties,
                "required": list(function_properties.keys()),
            },
        }
    ]

    prompt = f"""You are a professional Data Analyst / Data Miner and your job is to extract detailed information from documents.
            The document is as follows: {data}
            If a particular field is not found in the document, please return 'not found' for that field.
            """

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=function_descriptions,
        function_call="auto",
    )

    return response
