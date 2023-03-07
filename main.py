import openai
import click
import os
from termcolor import colored
from dotenv import load_dotenv, set_key

# Load environment variables from .env file
load_dotenv()

conversation_buffer = [{"role": "system", "content": "You are a helpful assistant."}]


# Define function to get API key from environment variables or prompt user for it
def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API key: ")
        set_key(".env", "OPENAI_API_KEY", api_key)
    return api_key

# Set up OpenAI API credentials
openai.api_key = get_api_key()

# Define function to generate text using GPT-3 API
def generate_text(prompt):
    conversation_buffer.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=conversation_buffer,
    )

    conversation_buffer.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

# Define CLI command using Click library
@click.command()
def prompt_user():
    while True:
        prompt = input("Enter a prompt: ")
        if not prompt:
            continue
        response = generate_text(prompt)
        response = colored(response, "green")
        print(response)

if __name__ == "__main__":
    prompt_user()

