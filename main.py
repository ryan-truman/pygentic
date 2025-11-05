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

def call_function(function_call, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    dispatch = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
    }
    kwargs = function_call.args
    kwargs["working_directory"] = "./calculator"
    if function_call.name not in dispatch:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": dispatch.get(function_call.name)(**kwargs)},
            )
        ],
    )

# response = client.models.generate_content(
#     model='gemini-2.0-flash-001',
#     contents=messages,
#     config=types.GenerateContentConfig(
#         tools=[available_functions],
#         system_instruction=system_prompt
#     )
# )

i=0

while i <= 20:
    i += 1
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    for candidate in response.candidates:
        messages.append(candidate.content)
    if "--verbose" in sys.argv:
        if response.function_calls:
            for function_call in response.function_calls:
                try:
                    output = call_function(function_call,verbose=True).parts[0].function_response.response
                    messages.append(
                        types.Content(
                            role="user",
                            parts=[types.Part.from_function_response(
                                name=function_call.name,
                                response=output
                            )]
                        )
                    )
                except Exception as e:
                    print(f"Error: {e}")
    else:
        if response.function_calls:
            for function_call in response.function_calls:
                try:
                    output = call_function(function_call).parts[0].function_response.response
                    messages.append(
                        types.Content(
                            role="user",
                            parts=[types.Part.from_function_response(
                                name=function_call.name,
                                response=output
                            )]
                        )
                    )
                except Exception as e:
                    print(f"Error: {e}")
    if not response.function_calls and response.text:
        print("Final response:\n" + response.text)
        break
