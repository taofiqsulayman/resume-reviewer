
# Resume Reviewer Application

## About the Project

The Resume Reviewer Application is a Streamlit-based web app designed to streamline the process of evaluating resumes. Users can upload one or multiple resumes in PDF or Excel format, and the application extracts key information such as candidate name, email, years of experience, previous companies, education, relevant skills, and suggests potential roles based on the provided skills and experience. The application leverages OpenAI's GPT model to process and extract meaningful insights from the resumes.

## Requirements

- Python 3.8 or higher
- Streamlit
- PyMuPDF (for PDF text extraction)
- pandas (for Excel file processing)
- OpenAI API Key

## Installation and Setup

1. **Clone the repository**
    ```sh
    git clone git@github.com:taofiqsulayman/portfolio-website.git
    cd resume-reviewer
    ```

2. **Create a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
    Create a `.env` file in the root of the project directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Run the Streamlit app**
    ```sh
    streamlit run app.py
    ```

## Usage

1. **Start the application**
    Open a terminal and navigate to the project directory. Run the Streamlit app using the command:
    ```sh
    streamlit run app.py
    ```

2. **Upload Resumes**
    - Go to the web interface that opens in your browser.
    - Upload one or multiple resumes in PDF or Excel format.
    - Ensure the OpenAI API Key field is populated (it will be auto-filled if set in the `.env` file).

3. **Submit and Review**
    - Click the 'Submit' button.
    - The application will process the uploaded files and display extracted information including candidate name, email, years of experience, previous companies, education, relevant skills, and suggested roles.

## File Structure

```
resume-reviewer/
├── .env                  # Environment variables
├── app.py                # Main Streamlit app
├── gpt.py                # OpenAI API interaction
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

## Requirements.txt

```
streamlit
pymupdf
pandas
openai
python-dotenv
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or issues, please reach out to:
- Taofiq A. at sulaymantaofiq@gmail.com
