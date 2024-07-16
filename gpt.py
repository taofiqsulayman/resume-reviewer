from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def get_gpt_response(data: str):
    function_descriptions = [
        {
            "name": "extract_resume_data",
            "description": "Extract information from resume.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Extract prospect name"},
                    "email": {
                        "type": "string",
                        "description": "Extract prospect email",
                    },
                    "years_of_experience": {
                        "type": "number",
                        "description": "Extract total years of experience",
                    },
                    "previous_companies": {
                        "type": "string",
                        "description": "Extract list of previous companies",
                    },
                    "education": {
                        "type": "string",
                        "description": "Extract education details",
                    },
                    "relevant_skills": {
                        "type": "string",
                        "description": "Extract relevant skills to the job",
                    },
                    "suggested_roles": {
                        "type": "string",
                        "description": "Suggest potential jobs/roles the individual can apply for, based on skills and experience",
                    },
                    "summary": {
                        "type": "string",
                        "description": "Summarize the resume",
                    },
                },
                "required": ["name", "email", "years_of_experience"],
            },
        }
    ]

    prompt = f"""You are a professional HR recruiter and your job is to extract detailed information from the prospect's resume.
            The prospect's resume is as follows: {data}
            """

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=function_descriptions,
        function_call="auto",
    )

    return response
