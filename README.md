# 🚀 AI Career Connect

Welcome to **AI Career Connect**! This is an AI-powered web application built with **Flask**, **SQLite**, and **Mistral AI**. It helps job seekers practice mock interviews using voice, analyze resumes, chat with an AI career coach, and track career progress on a dynamic dashboard.

---

## 🌟 What Does This Project Do?

Think of **AI Career Connect** as your personal 24/7 AI Career Assistant:

1. **🤖 AI Career Chat**: Ask any career or interview question. Mistral AI gives instant, helpful advice.
2. **🎙️ Voice Mock Interview**: Practice answering interview questions aloud. The app listens to your voice (**Speech-to-Text**) and speaks back to you (**Text-to-Speech**).
3. **📄 Resume Analyzer**: Paste your resume to get an instant match score (e.g. 85%) and suggestions to improve it for your dream job.
4. **📊 Dynamic Dashboard**: View live charts showing your career readiness score, mock interview history, and weekly practice activity.
5. **👤 User Profile & Accounts**: Create an account, sign in, and update your target job role (e.g. *Python Backend Developer*) and career goals.

---

## 📂 Project Structure Explained Simply

Here is what every folder and file in this project does:

```
AICareerConnect/
├── app/                        # Main folder containing all web app code
│   ├── __init__.py             # Starts the Flask app and connects database tables
│   ├── config.py               # Stores settings like database path and secret keys
│   ├── models/                 # Database structure (User, Chat logs, Interviews, Resumes)
│   ├── routes/                 # Handles web links/pages (/dashboard, /chat, /interview, /profile)
│   ├── services/               # Special helper logic (Mistral AI API, Speech-to-Text, Text-to-Speech)
│   ├── static/                 # Styles (CSS), JavaScript (JS), images, and uploaded files
│   └── templates/              # HTML webpage designs that you see in your browser
├── instance/                   # Folder where SQLite stores your local database file (app.db)
├── tests/                      # Automated test files to check if code works
├── .env.example                # Sample file for API keys
├── requirements.txt            # List of Python packages needed for this project
├── run.py                      # Main script you execute to launch the server
└── README.md                   # This beginner guide!
```

---

## 🚀 How to Run the App (Step-by-Step)

Follow these simple steps to start the application on your computer:

### Step 1: Open your Terminal / Command Prompt
Navigate to your project directory:
```bash
cd c:\Users\X1YOGA\OneDrive\Desktop\AICareerConnect
```

### Step 2: Install Required Libraries
Run this command to install Flask, SQLAlchemy, and AI tools:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
Start the Flask web server by typing:
```bash
python run.py
```

### Step 4: Open in Your Web Browser
Open your browser (Chrome, Edge, Firefox) and go to:
👉 **http://127.0.0.1:5000**

---

## 💡 How It Works Behind the Scenes

* **Backend Framework (Flask)**: Receives webpage requests from your browser and sends back responses.
* **Database (SQLite)**: Saves your user profile, chat history, and interview scores locally in `instance/app.db`.
* **AI Engine (Mistral API)**: Generates intelligent interview questions, resume scores, and career guidance.
* **Voice Engine (STT & TTS)**:
  * **Speech-to-Text (STT)**: Converts your spoken voice into text using microphone web APIs.
  * **Text-to-Speech (TTS)**: Converts AI text responses into audio voice playback.

---

## 🔑 Demo Account Quick Test

When you open `http://127.0.0.1:5000`, click **"One-Click Demo Account Login"** on the Sign In page to immediately try all features!
