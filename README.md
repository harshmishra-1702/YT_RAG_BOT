# YT_RAG_BOT 🤖📺

Built with the help of Sreamlit , just paste the url of the YouTube video and chat about it with the bot.

---

## 🛠️ Tech Stack & Architecture

* **Frontend Layer:** Streamlit (Dynamic, split-panel interactive dashboard)
* **Media Extraction:** yt-dlp (Programmatic native audio stream isolation)
* **Speech-to-Text:** AssemblyAI (Advanced deep-learning transcription with precise timestamps)
* **Orchestration:** LangChain LCEL (Semantic data chunking via RecursiveCharacterTextSplitter)
* **Vector Database:** FAISS + HuggingFace Embeddings (all-MiniLM-L6-v2)
* **Inference Engine:** Groq Cloud + llama-3.1-8b-instant (Ultra-low latency contextual answering)

---

## 🚀 Installation & Setup Guide

Follow these sequential steps to set up and run the application locally on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/harshmishra-1702/YT_RAG_BOT.git
```
```bash
cd YT_RAG_BOT
```
### 2. Set Up a Fresh Virtual Environment
To prevent hardcoded absolute path conflicts, initialize a clean local environment:
```bash
python -m venv venv
```
### 3. Activate the Environment
* On Windows (PowerShell):
  ```bash
  .\venv\Scripts\Activate.ps1
  ```
* On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install the required packages directly using the environment's Python interpreter to bypass launcher wrapping errors:
```bash
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```
### 5. Configure Environment Variables
Click here to login and get your -> [Groq API Key](https://console.groq.com/keys) for free.\
Click here to login and get your -> [Assembly AI API Key](https://www.assemblyai.com/dashboard/api-keys) for free .

Create a .env file in the root directory and add your API credentials:
```.env
GROQ_API_KEY=your_groq_api_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
```
---

## 🏃‍♂️ Running the Application

To bypass standard script wrapper path restrictions and ensure the app hooks perfectly into your local dependencies, launch Streamlit directly through your virtual environment's Python interpreter:

```bash
.\venv\Scripts\python.exe -m streamlit run app.py
```
Once running, the interactive dashboard will automatically open in your local browser. Paste a YouTube URL, let the transcription pipeline process the audio, and start querying the content!

---

  
