import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("missing api key")

    client = genai.Client(api_key=api_key)
    
    my_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    my_prompt = args.user_prompt

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    if args.verbose:
        print(f"User prompt: {my_prompt}")
        if response.usage_metadata == None:
            raise RuntimeError("API request failed")
        else:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"\n")

    function_results = []

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if not function_call_result.parts:
                raise Exception("No parts in function_call_result")
            
            first_part = function_call_result.parts[0]
            if first_part.function_response is None:
                raise Exception("Missing function_response")
            
            if first_part.function_response.response is None:
                raise Exception("Missing response in function_response")
            
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                resp = function_call_result.parts[0].function_response.response
                print(f"-> {resp.get("result")}")



if __name__ == "__main__":
    main()
