from flask import Flask, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")

groq_client = Groq(api_key=GROQ_API_KEY)

def generate_code_summary(code: str) -> str | None:
    """Generates a concise summary of the given code using the Groq API."""
    try:
        response = groq_client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following code:\n\n```\n{code}\n```",
                }
            ],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating code summary: {e}")
        return None

def check_code_completeness(code: str) -> str | None:
    """Checks if the given code snippet appears to be incomplete and suggests potential changes."""
    try:
        response = groq_client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze the following code snippet and determine if it appears to be incomplete. If it is, suggest potential ways to complete or improve it. If it appears complete, state that it seems complete.\n\n```\n{code}\n```",
                }
            ],
            max_tokens=200,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error checking code completeness: {e}")
        return None

@app.route('/summarize', methods=['POST'])
def summarize_code():
    """Endpoint to receive code and return its summary and completeness check."""
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({"error": "Missing 'code' in request body."}), 400

    code = data['code']
    summary = generate_code_summary(code)
    completeness_check = check_code_completeness(code)

    response = {}
    if summary:
        response['summary'] = summary
    else:
        response['summary'] = "Failed to generate code summary."

    if completeness_check:
        response['completeness_check'] = completeness_check
    else:
        response['completeness_check'] = "Failed to check code completeness."

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)