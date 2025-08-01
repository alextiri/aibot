import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]

verbose_mode = "--verbose" in sys.argv

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)



def main():
    if len(sys.argv) == 1:
        print("No prompt provided")
        exit(1)
    
    prompt_tokens = 0
    response_tokens = 0

    for i in range(0, 20):
        try:
            response = client.models.generate_content(
                model = 'gemini-2.0-flash-001',
                contents = messages,
                config = types.GenerateContentConfig(
                    tools= [available_functions], system_instruction=system_prompt
                    )
                )

            for candidate in response.candidates:
                messages.append(candidate.content)

            if response.function_calls:
                for function_call in response.function_calls:
                    print(f"- Calling function: {function_call.name}")
                    output = call_function(function_call, verbose=verbose_mode)
                    wrapped = types.Content(
                        role="tool",
                        parts=[
                            types.Part(
                                function_response = types.FunctionResponse(
                                    name = function_call.name,
                                    response = output
                                )
                            )
                        ]
                    )
                    messages.append(wrapped)
                    if not wrapped.parts[0].function_response.response:
                        raise Exception("Something went wrong...")
                    if verbose_mode:
                        print(f"-> {wrapped.parts[0].function_response.response}")
                    else:
                        print(wrapped.parts[0].function_response.response)
            
            if response.text:
                print(response.text)
                return

            prompt_tokens += response.usage_metadata.prompt_token_count
            response_tokens += response.usage_metadata.candidates_token_count

        except Exception as e:
            print(f'Error: {e}')
    
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
