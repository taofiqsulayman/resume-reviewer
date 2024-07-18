from __future__ import annotations

import streamlit as st
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import openai
from gpt import get_gpt_response
import pytesseract
from PIL import Image
import io
import pandas as pd
import json
import csv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_data(data: str, instructions: list) -> dict | None:
    gpt_response = get_gpt_response(data, instructions)
    response_message = gpt_response.choices[0].message
    reviews = response_message.function_call
    result = reviews.arguments
    if reviews and isinstance(result, dict):
        return result

    if reviews and isinstance(result, str):
        try:
            json_result = json.loads(result)
            return json_result
        except json.JSONDecodeError as e:
            print("Error: Cannot be converted to a JSON object.")
            print(e)
    return None


def extract_text_from_images(images) -> str:
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

# Streamlit configuration
st.set_page_config(page_title="Data Extraction App", page_icon="📜")
st.title("Data Extraction Application")
st.markdown(
    "This application extracts information from documents using OpenAI's GPT-3 model."
)

# Initialize session state for instructions
if "instructions" not in st.session_state:
    st.session_state["instructions"] = []

# Section for adding extraction instructions
st.subheader("Extraction Instructions")
st.markdown(
    "Add instructions for extracting information from the document. The title should be unique."
)

with st.form(key="instruction_form"):
    title = st.text_input("Title")
    data_type = st.selectbox("Data Type", ["string", "number"])
    description = st.text_area("Description")
    add_button = st.form_submit_button("Add")

    if add_button and title and data_type and description:
        st.session_state["instructions"].append(
            {"title": title, "data_type": data_type, "description": description}
        )

# Define a CSS style for the card
card_style = """
<style>
.card {
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    padding: 10px;
    margin-bottom: 10px; /* Space between cards */
}
.card:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
</style>
"""

st.markdown(card_style, unsafe_allow_html=True)

if st.session_state["instructions"]:
    st.subheader("Added Instructions")
    for instruction in st.session_state["instructions"]:
        st.markdown(
            f"<div class='card' style='display: flex; align-items: center;'><div style='flex-grow: 1;' title='{instruction['description']} ({instruction['data_type']})'>{instruction['title']}</div></div>",
            unsafe_allow_html=True,
        )

# File uploader and submit button
with st.form(key="resume_form"):
    files = st.file_uploader(
        "Add file(s) in PDF or CSV format:",
        type=["pdf", "csv"],
        accept_multiple_files=True,
    )
    submitted = st.form_submit_button("Submit")

if files:
    extracted_texts = []
    for file in files:
        if file.type == "application/pdf":
            pdf = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page in pdf:
                text += page.get_text()
                images = page.get_images(full=True)
                for img in images:
                    xref = img[0]
                    base_image = pdf.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    text += extract_text_from_images([image])
            extracted_texts.append(text)
        elif file.type == "text/csv":
            df = pd.read_csv(file)
            for index, row in df.iterrows():
                name = row["Name"]
                resume = row["Resume"]
                extracted_texts.append(f"{name}\n{resume}")

    responses = []
    for text in extracted_texts:
        file_data = extract_data(text, st.session_state["instructions"])
        responses.append(file_data)

    # Convert responses to CSV
    csv_data = []
    for idx, data in enumerate(responses):
        if data:
            row = {}
            for instruction in st.session_state["instructions"]:
                title = instruction["title"]
                formatted_title = title.lower().replace(" ", "_")
                row[title] = data.get(formatted_title)
            csv_data.append(row)

    # Display summary of the CSV data
    if csv_data:
        st.subheader("CSV Summary")
        st.write(pd.DataFrame(csv_data))

    # Download CSV file
    # if csv_data:
    #     with st.form(key="download_form"):
    #         download_button = st.form_submit_button("Download CSV")

    #     if download_button:
    #         csv_file = "data.csv"
    #         df = pd.DataFrame(csv_data)
    #         df.to_csv(csv_file, index=False)

    #         st.download_button("Download CSV", csv_file)
    else:
        st.markdown("No data extracted")
