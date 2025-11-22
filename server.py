import time #for time measuring
import requests #for making request to ollama services
from flask import Flask, jsonify, request, render_template  #for using flasl Json structure and render the html page
from flask_cors import CORS # for bipassing browser security

#--- CONFIGURATION for Ollama--- 
OLLAMA_URL = "http://localhost:11434/api/generate" #ollama url
MODEL_NAME = "llama3" # model name

# Initialize Flask
app = Flask(__name__, template_folder='templates') #template folder for html files  

#enable CORS
CORS(app)

#   Logs
def log(msg):
    
    print(f"[DEBUG] {msg}")


#--- ROUTES ---
@app.route('/') #for home route
def home():
    
    return render_template('index.html') #server homepage

#for speech
@app.route('/process_speech', methods=['POST']) 

def process_speech():
    #start time
    start_time = time.time()
    
   
    try:
        data = request.json
        user_text = data.get('text', '').strip()


        log(f"Request Received. User said: '{user_text}'") #for logs
        
        if not user_text:
            log("Empty text received. Ignoring.") #for logs
            return jsonify({'reply': ""})

    except Exception as e:
        log(f"Error parsing request: {e}") #for logs
        return jsonify({'error': 'Bad Request'}), 400

# trun all to lower case and chcek
    lower_text = user_text.lower()
    
    if lower_text in ['stop', 'quiet', 'shut up', 'exit', 'cancel']:
        log("Stop command detected.") #for logs
        return jsonify({'reply': "Okay, stopping."})
    
    if lower_text in ['hi', 'hello', 'hey']:
        return jsonify({'reply': "Hello! How can I help you today?"})
    
    #--- Ollama payload ---
    payload = {"model": MODEL_NAME, "prompt": user_text, "stream": False}

    log(f"Sending to Ollama ({MODEL_NAME})...") #for logs

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=10)

        if resp.status_code == 200:
            reply = resp.json().get("response", "")
            log(f"Received response from Ollama in {time.time() - start_time:.2f} seconds.") #for logs
            return jsonify({'reply': reply})
        else:
            log(f"Ollama returned status code {resp.status_code}.") #for logs
            return jsonify({'reply': "I had a network error."})
        
    except Exception as e:
        log(f"Error communicating with Ollama: {e}") #for logs
        return jsonify({'reply': "I cannot reach the AI model. Is Ollama running?"})




#--- RUN SERVER ---
if __name__ == '__main__':
     print(" SERVER RUNNING on http://localhost:5000")
    
    # debug= true as allow auto relaod
     app.run(host='0.0.0.0', port=5000, debug=True)