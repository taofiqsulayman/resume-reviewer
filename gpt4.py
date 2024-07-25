# from gpt4all import GPT4All

# def sample_gpt4all() -> None:
#   model = GPT4All(model_name="Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", model_path="/Users/seamhealth/Library/Application Support/nomic.ai/GPT4All")
#   print(model.generate("quadratic formula"))


# from gpt4all import GPT4All


  
# from gpt4all import GPT4All

# model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf") # downloads / loads a 4.66GB LLM
# with model.chat_session():
#     print(model.generate("How can I run LLMs efficiently on my laptop?", max_tokens=1024))

    # # Initialize the model with the specified name and path
    # model = GPT4All(model_name="Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf", model_path="/Users/seamhealth/Library/Application Support/nomic.ai/GPT4All")

    # # Generate a response from the model
    # input_text = "Hello, I'm a GPT-4-like model running locally."
    # response = model.generate(input_text)

    # # Print the generated response
    # print(response)



# def get_gpt_response(data: str):
#     function_descriptions = [
#         {
#             "name": "extract_resume_data",
#             "description": "Extract information from resume.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "name": {"type": "string", "description": "Extract prospect name"},
#                     "email": {
#                         "type": "string",
#                         "description": "Extract prospect email",
#                     },
#                     "years_of_experience": {
#                         "type": "number",
#                         "description": "Extract total years of experience and take the dates into account",
#                     },
#                     "previous_experience": {
#                         "type": "string",
#                         "description": "Extract list of previous companies or experience",
#                     },
#                     "education": {
#                         "type": "string",
#                         "description": "Extract education details",
#                     },
#                     "relevant_skills": {
#                         "type": "string",
#                         "description": "Extract relevant skills to the job",
#                     },
#                     "suggested_roles": {
#                         "type": "string",
#                         "description": "Suggest potential jobs/roles the individual can apply for, based on skills and experience",
#                     },
#                     "summary": {
#                         "type": "string",
#                         "description": "Summarize the resume",
#                     },
#                 },
#                 "required": ["name", "email", "years_of_experience"],
#             },
#         }
#     ]

#     prompt = f"""You are a professional HR recruiter and your job is to extract detailed information from the prospect's resume.
#             The prospect's resume is as follows: {data}
#             """

#     messages = [{"role": "user", "content": prompt}]

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         functions=function_descriptions,
#         function_call="auto",
#     )

#     return response
