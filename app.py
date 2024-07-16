from __future__ import annotations

import streamlit as st
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import openai
from gpt import get_gpt_response

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_resume_data(data: str) -> dict | None:
    gpt_response = get_gpt_response(data)
    response_message = gpt_response.choices[0].message
    reviews = response_message.function_call
    result = reviews.arguments
    if reviews and isinstance(result, dict):
        return result

    if reviews and isinstance(result, str):
        import json

        try:
            json_result = json.loads(result)
            return json_result
        except json.JSONDecodeError as e:
            print("Error: Cannot be converted to a JSON object.")
            print(e)
    return None


# Streamlit configuration
st.set_page_config(page_title="Resume Reviewer", page_icon="")
st.title("Resume Reviewer")
st.markdown(
    "Use this application to review resumes and extract detailed information from them."
)

with st.form(key="resume_form"):
    files = st.file_uploader(
        "Add the resume(s) in PDF or Excel format:",
        type=["pdf", "xlsx"],
        accept_multiple_files=True,
    )
    # openai_api_key = st.text_input(
    #     "OpenAI API Key",
    #     type="password",
    #     value=os.getenv("OPENAI_API_KEY", ""),
    #     help="Add the OpenAI API key here.",
    # )
    submitted = st.form_submit_button("Submit")

if files:
    extracted_texts = []
    for file in files:
        if file.type == "application/pdf":
            pdf = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in pdf:
                text += page.get_text()
            extracted_texts.append(text)
        elif (
            file.type
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            import pandas as pd

            df = pd.read_excel(file)
            for index, row in df.iterrows():
                extracted_texts.append(
                    "\n".join(str(value) for value in row if pd.notnull(value))
                )

    responses = []
    for text in extracted_texts:
        resume_data = extract_resume_data(text)
        responses.append(resume_data)

    for idx, resume_data in enumerate(responses):
        st.markdown(f"### Resume {idx + 1} Review")
        if resume_data:
            st.markdown(f"**Name:** {resume_data.get('name')}")
            st.markdown(f"**Email:** {resume_data.get('email')}")
            st.markdown(
                f"**Years of Experience:** {resume_data.get('years_of_experience')}"
            )
            st.markdown(
                f"**Previous Experience:** {resume_data.get('previous_experience')}"
            )
            st.markdown(f"**Education:** {resume_data.get('education')}")
            st.markdown(f"**Relevant Skills:** {resume_data.get('relevant_skills')}")
            st.markdown(f"**Suggested Roles:** {resume_data.get('suggested_roles')}")
            st.markdown(f"**Summary:** {resume_data.get('summary')}")
        else:
            st.markdown("No data extracted")
