from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
sys_file_path = 'analysis/system.md'
filepath = '1w-claude-sonn-30'

file_names = []

for filename in os.listdir(filepath):
    if filename.endswith('.md'):  # Check for files ending with .md
        file_names.append(filename)

    with open(sys_file_path, 'r') as file:
        system = file.read()

for filename in file_names:

    with open(f'{filepath}/{filename}', 'r') as file:
        content = file.read()

    LANG_PROMPT_TEMPLATE = """
    Summarize based on the following background

    {system}

    Here is the text to be summarized:

    {content}

    """

    model = GoogleGenerativeAI(
            model="gemini-pro",
            max_output_tokens=1024,
            google_api_key=os.environ["GOOGLE_API_KEY"]
        )

    prompt_template = ChatPromptTemplate.from_template(LANG_PROMPT_TEMPLATE)

    chain_with_prompt = prompt_template | model | StrOutputParser()

    result = chain_with_prompt.invoke({"system": system, "content": content})

    with open(f'{filepath}-summary/{filename}', 'w') as file:
        file.write(result)