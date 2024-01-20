import os
from openai import OpenAI

try: 
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print("Warning -- dotenv could not be imported, will use default environment variables")

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
default_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

prompt_template = """
You are a educational content creator and you are trying to explain the following complicated concept to a general audience . 
Please extract key information and then simplify and summarize the following text:

-- TEXT START --
{text}
-- TEXT END --

Output the simplified text below as a narration script for voice over in the following format:\n\n

[
    {{
        "idx": number,
        "text": text,
        "highlight": [important words in text],
        "image": description
    }},
]

Each scene should be at most two sentences long.
The first scene should be an interesting hook for audience.
The last scene should be a profound relevation.
Highlight the most important part of the text. 
Write at least 8 scenes.
"""
