# Doctor's Office Agent to Agents
Welcome to **Doctor Office A2A**. I created this project to demonstrate a distributed multi-agent system where each agent runs on its own device, but they all communicate via Agent-to-Agent (A2A) protocols.

## The Agents

### 1. Doctor Office Agent (`doctor_office/`)
- **Model:** `functiongemma:270m` (via Ollama)
- **Hardware:** Extremely lightweight. I actually ran this on my old phone via Termux! It's perfect for an older clinic PC.
- **Role:** Registers patients and serves a local dashboard. Keeps everything private and local.

### 2. MedGemma Agent (`medgemma/`)
- **Model:** `medgemma-4b` (via Ollama)
- **Hardware:** Resource intensive. Needs a PC with >4GB VRAM GPU, an M-series Mac, or a cloud instance like Google Colab.
- **Role:** Provides preliminary medical guidance based on symptoms.
- **Note:** If your hardware can't handle it, you can skip running this agent. Just update the WhatsApp agent's instructions to remove the consultation step.

### 3. WhatsApp Orchestrator Agent (`whatsapp/`)
- **Model:** `gemini-3-flash-preview` (via Google AI Studio)
- **Platform:** Served via Agno's AgentOS WhatsApp interface.
- **Role:** The user-facing interface. It chats with the user and coordinates the other two agents.
- **Deployment:** Can be deployed on a server, cloud function, or locally.

## How to Run

You can run these agents on different devices (e.g., Doctor Office on a clinic PC, MedGemma on Colab, WhatsApp Agent on a server).

**Crucial Step:** If you're splitting them up, you **must** update the base addresses in `whatsapp/agent.py` to point to the actual IP addresses of the other agents.

### Running Locally (The Easy Way)
To save time, you can just create one virtual environment for the whole project instead of three separate ones.

1. **Setup the Environment**
   ```bash
   # Create one venv in the root
   python -m venv .venv
   . .venv/Scripts/activate  # Windows (PowerShell)
   # source .venv/bin/activate # Mac/Linux

   # Install dependencies for everyone
   pip install -r medgemma/requirements.txt
   pip install -r doctor_office/requirements.txt
   pip install -r whatsapp/requirements.txt
   ```

2. **Run the Agents** (Open 3 separate terminals, activate the venv in each, and go!)

   **Terminal 1: MedGemma** (Port 7778)
   ```bash
   cd medgemma
   python medgemma.py
   ```

   **Terminal 2: Doctor Office** (Port 7779)
   ```bash
   cd doctor_office
   python doctor_office_agent.py
   ```

   **Terminal 3: WhatsApp Orchestrator** (Port 7777)
   ```bash
   cd whatsapp
   $env:GOOGLE_API_KEY="<your_api_key>"
   python agent.py
   ```

