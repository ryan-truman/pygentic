import os
import sys
import config
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
github_pat = os.environ.get("GITHUB_PAT_TOKEN")
system_prompt = config.system_prompt

client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
)

def call_function(function_call, verbose=False):
    dispatch = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file_content": write_file_content,
    "run_python": run_python,
    }
    dispatch.get(function_call.name)("./calculator", function_call.args)


print(response.function_calls)
for function_call in response.function_calls:
    print(function_call)
    call_function(function_call)
    print(f"Calling function: {function_call.name}({function_call.args})")

if "--verbose" in sys.argv:
    print(f"{response.text}\nUser prompt: {sys.argv[1]}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
else:
    print(response.text)
