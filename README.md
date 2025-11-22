# Real-Time-Interruptible-Voice-AI-Agent
Real-Time Interruptible Voice AI Agent You can talk and then Interupt it anytime ask again and go ahead.
🎙️ Interruptible Voice-Based Conversational Agent
A full-stack voice agent capable of real-time conversation and immediate interruption.
This project uses a Flask (Python) backend to communicate with a local LLM (Ollama) and a Web-based Frontend to handle asynchronous audio streams, ensuring that the user can cut the bot off mid-sentence naturally.
📋 Prerequisites
Before running the project, ensure you have the following installed on your system:
1.	Anaconda or Miniconda: Download Here
2.	Ollama: Download Here
o	Note: This project uses the llama3 model.
⚙️ Step 1: Environment Setup (Conda)
To ensure the project runs on any machine, we use a Conda environment.
1.	Open your Terminal or Anaconda Prompt.
2.	Navigate to the project folder where environment.yml is located.
3.	Run the following command to create the environment:
4.	conda env create -f environment.yml
5.	Activate the new environment:
6.	conda activate voice_agent
🧠 Step 2: Setup the LLM (Ollama)
The Python backend needs to talk to a local AI model.
1.	Open a separate terminal window.
2.	Run the following command to pull the Llama 3 model:
3.	ollama pull llama3
4.	Start the Ollama server:
5.	ollama serve
(Keep this terminal window open in the background)
![Place screenshot of Ollama running in terminal here]
🚀 Step 3: Project Structure
Ensure your folder looks exactly like this. The index.html file must be inside a folder named templates.
/Project_Folder
  ├── templates/
  │     └── index.html      <-- Your Frontend Code
  ├── server.py             <-- Your Backend Code
  ├── environment.yml       <-- Config file
  └── README.md
▶️ Step 4: Run the Application
1.	In your main terminal (where you activated voice_agent), run the server:
2.	python server.py
You should see a message saying: SERVER RUNNING on http://0.0.0.0:5000
![Place screenshot of Python Server Running here]
3.	Open your Google Chrome browser.
4.	Go to: http://localhost:5000
🎮 Usage Guide
1.	Click "Start Agent": The browser will ask for Microphone permissions. Click Allow.
2.	Speak: Say "Hello" or ask a question.
3.	Interrupt: While the AI is speaking, simply start talking again (e.g., "Wait, stop!").
o	The visual interface will turn Red.
o	The audio will cut off immediately.
o	The agent will listen to your new command.
![Place screenshot of the Web Interface here]
🛠️ Troubleshooting
•	"Speech Error: no-speech": This usually means your microphone is muted or Chrome is looking at the wrong device. Check chrome://settings/content/microphone.
•	"Cannot connect to Ollama": Ensure you ran ollama serve in a separate window.

