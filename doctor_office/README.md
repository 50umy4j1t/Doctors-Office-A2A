# Doctor Office Agent

A minimal office assistant that registers patient records and serves a simple dashboard. Runs a FastAPI app and persists patients to `patients.json` alongside this file.

## Prerequisites
- Python 3.10+
- Ollama installed and running (for the lightweight model used by this agent)
  - Model: `functiongemma:270m` (referenced by `Ollama(id="functiongemma:270m")`)

## Setup
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```bash
python doctor_office_agent.py
```
- Default port: 7779
- Endpoints:
  - `/patientspage` serve the dashboard HTML
  - Static assets mounted at `/static`

## About the Model: FunctionGemma 🧠
This agent runs on **FunctionGemma** (specifically the `270m` version), which is a super lightweight model from Google designed specifically for function calling. It's small enough to run on edge devices like old phones or laptops but powerful enough to handle structured data tasks like registering patients.

Check out the details here:
- [FunctionGemma Docs](https://ai.google.dev/gemma/docs/functiongemma)
- [Google Blog Post](https://blog.google/technology/developers/functiongemma/)
- [Hugging Face Model Card](https://huggingface.co/google/functiongemma-270m-it)
- [Ollama Library](https://ollama.com/library/functiongemma)

## Notes
- Patient data is stored in `patients.json` in this folder.
- This agent exposes an A2A endpoint via Agno AgentOS and is designed to be driven by another agent (e.g., the WhatsApp agent) with strictly formatted messages.
- I built this in a single day with the goal of running it on my old phone, which is why I went with a rough HTML and JSON setup. In a real-world application—ideally running on an old PC or laptop- I'd use an SQL database (like MySQL or SQLite) and add features like patient search history and a full EHR like system.