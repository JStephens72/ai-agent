import argparse
import os
import sys
import pprint

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from config import MAX_ITERS
from prompts import system_prompt

def get_response(client, messages, available_functions, system_prompt, verbose):
   
    genai_response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    pprint.pp(genai_response)

    if not genai_response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if verbose:
        print(f"Prompt tokens: {genai_response.usage_metadata.prompt_token_count}\n")
        print(f"Response tokens: {genai_response.usage_metadata.candidates_token_count}\n")
    
    candidates = genai_response.candidates
    if candidates:
        for candidate in candidates:
            messages.append(candidate.content)

    if not genai_response.function_calls:
        return genai_response.text
    
    function_results = []
    for function_call in genai_response.function_calls:
        function_call_result = call_function(function_call, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            or not function_call_result.parts[0].function_response.response
        ):
            raise Exception("Bad function response")

        first_part = function_call_result.parts[0]
        function_results.append(first_part)
                                 
    messages.append(types.Content(role="user", parts=function_results))

    return None
                


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    if args.verbose:
        print(f"User prompt: {user_prompt}\n")

    for _ in range(MAX_ITERS):
        final_text = get_response(
            client=client, 
            messages=messages, 
            available_functions=available_functions, 
            system_prompt=system_prompt, 
            verbose=args.verbose
        )
        
        if final_text is not None:
            print("Final response:\n")
            print(final_text)
            return
        
    print(f"Maximum interations ({MAX_ITERS}) reached without a final response")
    sys.exit(1)



if __name__ == "__main__":
    main()
