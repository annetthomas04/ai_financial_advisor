from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for local frontend testing

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# -------- Helper Function --------
def query_deepseek(prompt: str, max_retries=2):
    """Send user prompt to DeepSeek API and return the assistant's reply."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    # List of models to try in order of preference
    models = [
        "deepseek/deepseek-r1:free",
        "mistralai/mistral-7b-instruct:free",  # Alternative free model
        "google/palm-2-chat-bison:free"        # Another alternative
    ]
    
    system_prompt = (
        "You are a professional AI financial advisor. "
        "You give helpful, actionable financial insights, "
        "budgeting suggestions, and lifestyle-based money tips. "
        "Keep your responses concise, clear, and friendly."
    )

    # Try each model with retries
    for model in models:
        retries = 0
        while retries <= max_retries:
            try:
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                }
                
                print(f"Trying model: {model}, attempt {retries+1}")
                response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
            except requests.exceptions.HTTPError as e:
                # More detailed logging for API errors
                print(f"API request failed with status {response.status_code}: {e}")
                try:
                    error_data = response.json()
                    print(f"Response body: {error_data}")
                    
                    # Check if this is a rate limit error
                    if response.status_code == 429:
                        if retries < max_retries:
                            import time
                            wait_time = (retries + 1) * 2  # Exponential backoff: 2s, 4s
                            print(f"Rate limited. Waiting {wait_time} seconds before retry...")
                            time.sleep(wait_time)
                            retries += 1
                            continue
                        else:
                            # If we've exhausted retries for this model, try the next one
                            break
                except:
                    print(f"Raw response: {response.text}")
                
                # For non-rate-limit errors, or if we've exhausted retries, try next model
                break
                
            except requests.exceptions.RequestException as e:
                print("API connection failed:", e)
                # For connection errors, try next model
                break
    
    # If we've tried all models and still failed
    return "⚠️ The AI service is currently unavailable. Our models are experiencing high demand. Please try again in a few minutes."

# -------- Routes --------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Financial Advisor API is running 🚀"})

@app.route("/chat", methods=["POST"])
def chat():
    """Receive user input and return DeepSeek's response."""
    user_input = request.json.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    print(f"User message: {user_input}")

    # Context prompt: personalize for financial topics
    prompt = f"User says: {user_input}. Provide a financial tip or insight relevant to this query."
    ai_reply = query_deepseek(prompt)

    return jsonify({"response": ai_reply})

# -------- Main Entry Point --------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
