import time
import requests  # pip install requests
from flask import Flask, render_template, request, jsonify  # pip install flask
from flask_cors import CORS  # pip install flask-cors

# --- CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"  # Ensure you have run 'ollama pull llama3'

# Initialize Flask
# template_folder='templates' tells Flask to look for HTML files in the 'templates' folder
app = Flask(__name__, template_folder='templates')

# Enable CORS (Cross-Origin Resource Sharing)
# This allows the frontend to communicate with the backend without security errors,
# even if you decide to use Live Server later.
CORS(app)

# --- HELPER FUNCTIONS ---
def log(msg):
    """Simple logging function to print to the terminal with a tag."""
    print(f"[DEBUG] {msg}")

# --- ROUTES ---

@app.route('/')
def home():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/process_speech', methods=['POST'])
def process_speech():
    """Receives text from the frontend, sends it to Ollama, and returns the response."""
    start_time = time.time()
    
    # 1. Receive and Parse Data
    try:
        data = request.json
        user_text = data.get('text', '').strip()
        log(f"📨 Request Received. User said: '{user_text}'")
        
        if not user_text:
            log("⚠️ Empty text received. Ignoring.")
            return jsonify({'reply': ""})

    except Exception as e:
        log(f"❌ Error parsing request: {e}")
        return jsonify({'error': 'Bad Request'}), 400

    # 2. Local Rules (Fast responses for specific commands)
    lower_text = user_text.lower()
    
    # Check for stop commands
    if lower_text in ['stop', 'quiet', 'shut up', 'exit', 'cancel']:
        log("🛑 Stop command detected.")
        return jsonify({'reply': "Okay, stopping."})
    
    # Check for greetings
    if lower_text in ['hi', 'hello', 'hey']:
        return jsonify({'reply': "Hello! How can I help you today?"})

    # 3. Send to Ollama (The "Brain")
    log(f"🧠 Sending to Ollama ({MODEL_NAME})...")
    
    payload = {
        "model": MODEL_NAME, 
        "prompt": user_text, 
        "stream": False
    }

    try:
        # Timeout set to 30s in case the model is slow to load or generate
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            # Extract the actual text response from Ollama's JSON
            reply_text = response.json().get('response', '')
            duration = round(time.time() - start_time, 2)
            
            log(f"✅ Ollama replied in {duration}s. Length: {len(reply_text)} chars")
            # log(f"📝 Full Reply: {reply_text}") # Uncomment to see full text in terminal
            
            return jsonify({'reply': reply_text})
        else:
            log(f"⚠️ Ollama Error Status: {response.status_code}")
            return jsonify({'reply': "I had trouble thinking of an answer."})

    except requests.exceptions.ConnectionError:
        log("❌ CRITICAL: Could not connect to Ollama. Is 'ollama serve' running?")
        return jsonify({'reply': "I cannot reach my brain. Please check if Ollama is running."})
        
    except Exception as e:
        log(f"❌ Unexpected Error: {e}")
        return jsonify({'reply': "Something went wrong internally."})

# --- MAIN ENTRY POINT ---
if __name__ == '__main__':
    print("\n" + "="*50)
    print(" SERVER RUNNING on http://localhost:5000")
    print(f" Target LLM: {MODEL_NAME}")
    print(" Keep this window open to see Backend Logs")
    print("="*50 + "\n")
    
    # debug=True allows auto-reload when you change the code
    app.run(host='0.0.0.0', port=5000, debug=True)