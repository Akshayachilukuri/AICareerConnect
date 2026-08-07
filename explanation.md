# Senior Flask Developer Guide: Project Architecture Explanation

This document explains the technical design decisions and rationale behind every folder and file in the **AI Career Connect** project structure.

---

## Directory Tree

```
AICareerConnect/
├── app/                        # Primary Application Package
│   ├── __init__.py             # Application Factory initialization
│   ├── config.py               # Centralized Application Configuration
│   ├── models/                 # SQLAlchemy Database ORM Schemas
│   │   ├── __init__.py
│   │   ├── user.py             # User authentication and profile models
│   │   ├── chat.py             # Career chat message logs model
│   │   ├── interview.py        # Mock interview question & response model
│   │   └── resume.py           # Resume analysis score and feedback model
│   ├── routes/                 # Flask Blueprints (HTTP request controllers)
│   │   ├── __init__.py
│   │   ├── main.py             # Dynamic dashboard views & chart metrics JSON API
│   │   ├── auth.py             # User login, registration, and session routes
│   │   ├── ai.py               # Mistral AI interaction endpoints (Chat, Resume, Interview)
│   │   └── voice.py            # Speech-to-Text (STT) and Text-to-Speech (TTS) endpoints
│   ├── services/               # Independent Business & Service Layer
│   │   ├── __init__.py
│   │   ├── mistral_service.py  # Mistral API integration client with fallback generator
│   │   ├── stt_service.py      # Audio processing & Speech-to-Text transcript service
│   │   └── tts_service.py      # Text-to-Speech audio synthesis generator (gTTS)
│   ├── static/                 # Frontend Static Assets
│   │   ├── css/
│   │   │   ├── style.css       # Core modern CSS design system & glassmorphism theme
│   │   │   └── dashboard.css   # Dynamic dashboard grid layout and widget styles
│   │   ├── js/
│   │   │   ├── main.js         # Base UI scripts (dark mode, toasts, active states)
│   │   │   ├── dashboard.js    # Live Chart.js fetching and dynamic rendering logic
│   │   │   ├── voice.js        # Browser Web Speech API & voice recorder controller
│   │   │   └── ai_chat.js      # Interactive AI career assistant text/voice controller
│   │   └── uploads/            # Runtime storage directory for user audio/resumes
│   └── templates/              # Jinja2 HTML Layout Views
│       ├── base.html           # Master layout template (Navigation, sidebar, toast system)
│       ├── dashboard.html      # Dynamic career metrics & analytics view
│       ├── chat.html           # AI career Q&A chat interface (Text & Voice toggle)
│       ├── resume.html         # Resume upload & instant AI feedback center
│       ├── interview.html      # Voice mock interview practice studio
│       └── auth/
│           ├── login.html      # User login view
│           └── register.html   # User registration view
├── instance/                   # Runtime instance directory (Stores SQLite DB file: app.db)
├── tests/                      # Unit & integration test suites
│   ├── test_routes.py          # HTTP API endpoint tests
│   └── test_services.py        # Mistral, STT, and TTS service logic tests
├── .env.example                # Template file for secret keys and API keys
├── .gitignore                  # Git version control exclusions
├── requirements.txt            # Python dependencies manifest
├── run.py                      # Application entry point WSGI launcher
└── explanation.md              # Architectural justification guide
```

---

## Detailed Rationale: Why Each Folder Exists

### 1. `app/` (Application Core Package)
* **Why it exists:** Python packages group code into isolated namespaces. Wrapping all Flask code inside `app/` prevents global namespace pollution, eliminates circular imports, and allows running tests or background workers cleanly.

### 2. `app/__init__.py` (Application Factory)
* **Why it exists:** Implements the **Application Factory Pattern** (`create_app()`). Instead of creating a single global `app = Flask(__name__)` object, this function constructs app instances dynamically on demand. This allows isolation between production runs and automated test suites.

### 3. `app/config.py` (Configuration Management)
* **Why it exists:** Consolidates app settings (Secret keys, Database URIs, API keys, Upload directories). Keeping configurations centralized makes it easy to switch environments (Development, Testing, Production) without touching application code.

### 4. `app/models/` (Data & Database Layer)
* **Why it exists:** Implements the **Model-View-Controller (MVC)** data layer using Flask-SQLAlchemy ORM.
  * `user.py`: Encapsulates user profiles, password hashing, and target job roles.
  * `chat.py`: Stores user queries and AI responses for persistent chat history.
  * `interview.py`: Tracks mock interview sessions, questions asked, user answers, and AI scores.
  * `resume.py`: Stores resume evaluation metrics (Match score, skills identified, improvement suggestions).

### 5. `app/routes/` (Presentation & HTTP Controller Layer)
* **Why it exists:** Uses **Flask Blueprints** to group related HTTP routes. Blueprints allow large Flask applications to be split into manageable feature modules:
  * `main.py`: Handles dashboard views and returns dynamic JSON data for frontend live charts.
  * `auth.py`: Controls user authentication flows.
  * `ai.py`: Exposes endpoints for Mistral AI career coaching, resume parsing, and interview generation.
  * `voice.py`: Serves STT (Speech-to-Text audio upload handling) and TTS (synthesized audio stream playback).

### 6. `app/services/` (Business Logic Layer)
* **Why it exists:** Isolates third-party API logic and complex algorithms from HTTP view functions.
  * **Rule of Clean Code:** Routes should only handle request parsing and returning responses; business logic belongs in services!
  * `mistral_service.py`: Wraps Mistral AI HTTP requests (with automated fallback mechanisms if offline).
  * `stt_service.py`: Processes incoming audio blobs and converts speech to text.
  * `tts_service.py`: Converts text strings to `.mp3` audio binary data for voice playback.

### 7. `app/static/` (Frontend Asset Management)
* **Why it exists:** Standard location for serving CSS, client-side JS, icons, and uploaded files.
  * `css/`: Modular stylesheets adhering to design system guidelines.
  * `js/`: Modular JavaScript logic (`voice.js` for microphone audio APIs, `dashboard.js` for Chart.js rendering, `ai_chat.js` for streaming UI).
  * `uploads/`: Isolated temporary directory for processing uploaded resumes and recorded audio files.

### 8. `app/templates/` (Jinja2 View Templates)
* **Why it exists:** Houses Jinja2 HTML layout components. Uses **Template Inheritance** (`base.html`) so UI navigation, sidebar elements, footers, and scripts are defined once and reused everywhere.

### 9. `instance/` (Local Instance Storage)
* **Why it exists:** Flask convention for storing runtime database files (`app.db`) and local secrets. Is unversioned in Git so sensitive databases remain on local machines.

### 10. `tests/` (Automated Test Suite)
* **Why it exists:** Contains unit tests verifying API contracts, model relationships, and service fallbacks before deploying updates.

---

## Key Design Patterns Applied

1. **Application Factory Pattern**: Decouples app instantiation from server execution.
2. **Separation of Concerns (SoC)**: Views handle HTTP, Services handle logic, Models handle data.
3. **Blueprint Modular Architecture**: Scalable route design pattern for enterprise Flask apps.
4. **Fallback & Resiliency**: Mistral AI and STT/TTS services feature intelligent fallbacks so the app operates flawlessly even in low-connectivity or unconfigured key environments.
