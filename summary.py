import os
import sys
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load API Key securely
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Set it in your environment variables.")

# Use an updated model (Check Groq's latest available models)
llm = ChatGroq(model="llama3-8b-8192", temperature=0.7)  # Example model, update as needed

def summarize_code(code_snippet):
    """Summarizes a given Python code snippet using Groq's LLM."""
    prompt = f"""
    You are an AI assistant specializing in summarizing Python code. 
    Given a Python function, explain its purpose clearly and concisely.

    Example 1:
    Code:
    ```python
    def add(a, b):
        return a + b
    ```
    Summary: This function takes two numbers and returns their sum.

    Example 2:
    Code:
    ```python
    def is_even(n):
        return n % 2 == 0
    ```
    Summary: This function checks if a number is even and returns True if it is, otherwise False.

    Now, summarize the following code:
    ```python
    {code_snippet}
    ```

    Summary:
    """
    try:
        return llm.invoke(prompt)  # Use invoke instead of predict/apredict
    except Exception as e:
        return f"Error generating summary: {e}"

print("Enter your Python code snippet (Press Enter twice to finish):")
user_code = []
while True:
    line = input()
    if line == "":
        break
    user_code.append(line)

user_code_snippet = "\n".join(user_code)

if not user_code_snippet.strip():
    print("No code provided.")
else:
    summary = summarize_code(user_code_snippet)
    print("Code Summary:", summary)
