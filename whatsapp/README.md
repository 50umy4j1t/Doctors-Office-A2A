# WhatsApp Orchestrator Agent

A WhatsApp-facing agent that coordinates with the MedGemma advisor and the Doctor Office agent via A2A JSON-RPC calls.

## Prerequisites
- Python 3.10+
- Google Gemini API Key available in environment: `GOOGLE_API_KEY`
- WhatsApp interface credentials. You'll need to set up a Meta developer account and get your credentials by following the instructions [here](https://github.com/agno-agi/agno/tree/main/cookbook/06_agent_os/interfaces/whatsapp#getting-whatsapp-credentials).
- Ensure downstream agents are running and reachable at the hardcoded URLs or change the base url to your running instances of those agents:
  - MedGemma: `http://localhost:7778/a2a/agents/medgemma_agent/v1/message:send`
  - Doctor Office: `http://localhost:7779/a2a/agents/doctor_office_agent/v1/message:send`

## Setup
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```bash
$env:GOOGLE_API_KEY="<your_api_key>"  # PowerShell example
python agent.py
```
- Default port: 7777

## Notes
- This agent provides a WhatsApp interface via Agno. Consult your Agno WhatsApp docs for webhook/tunnel configuration and required environment variables.
- The agent uses the Google Gemini model via `agno.models.google.Gemini`.