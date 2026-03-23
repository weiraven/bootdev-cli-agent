import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Argument parsing
    parser = argparse.ArgumentParser(description="Gemini CLI Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found. Make sure it is set in your .env file.")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(
            role="user", 
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt),
    )

    if response.usage_metadata is None:
        raise RuntimeError(
            "No usage metadata returned. The API request may have failed."
        )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    print("Response:")

    function_responses = []
    
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)

            if not function_call_result.parts:
                raise RuntimeError("Function call result has no parts")
            
            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise RuntimeError("Function call result part has no function_response")
            
            if function_response.response is None:
                raise RuntimeError("Function response has no response payload")
            
            function_responses.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
