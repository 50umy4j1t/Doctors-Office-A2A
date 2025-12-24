import uuid

import requests
from agno.agent import Agent
from agno.models.google import Gemini
from agno.os import AgentOS
from agno.os.interfaces.whatsapp import Whatsapp

# --- 1. A2A Helper Function (The Protocol) ---
def _send_a2a_message(url: str, text: str) -> str:
    """
    Internal helper to send a message using your A2A JSON-RPC format.
    """
    payload = {
        "id": "trip_planner_client",
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "message_id": str(uuid.uuid4()),
                "role": "user",
                "parts": [{"text": text}],
            }
        },
    }

    try:
        # Send POST request
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Unwrap the specific A2A response structure
        # result -> history -> last_item -> parts -> first_item -> text
        if "result" in data and "history" in data["result"]:
            history = data["result"]["history"]
            if history:
                last_msg = history[-1]
                if "parts" in last_msg and last_msg["parts"]:
                    return last_msg["parts"][0]["text"]

        return f"System Error: The agent at {url} responded, but no text message was found in the history."

    except Exception as e:
        return f"Connection Error: Could not talk to agent at {url}. Details: {e}"


# --- 2. Tool functions ---


def medgemma_consult(symptoms: str) -> str:
    """Ask the MedGemma agent for a quick symptoms assessment."""
    MEDGEMMA_URL = "http://localhost:7778/a2a/agents/medgemma_agent/v1/message:send" #insert address
    return _send_a2a_message(MEDGEMMA_URL, symptoms)


def doctor_office_notify(patient_name: str, illness_summary: str, description: str = "") -> str:
    """Notify the doctor office agent with patient details."""
    DOCTOR_URL = "http://localhost:7779/a2a/agents/doctor_office_agent/v1/message:send"
    payload_text = f"PATIENT: {patient_name}\nILLNESS: {illness_summary}"
    if description:
        payload_text += f"\nDESCRIPTION: {description}"
    return _send_a2a_message(DOCTOR_URL, payload_text)



chat_agent = Agent(
    name="Doctor office assistant",
    id="text_chat",
    model=Gemini(id="gemini-3-flash-preview"),
    # Give the agent the tools we just created
    tools=[
        medgemma_consult,
        doctor_office_notify,
    ],
    markdown=True,
    description="You are an whatsapp assistant",
    instructions=["""### ROLE & PERSONA
You are a "Personal Health Buddy," a friendly, familiar AI assistant living on WhatsApp. 
- **Tone:** Casual, empathetic, warm, and concise (WhatsApp style). Use emojis sparingly but effectively 🌿.
- **Goal:** Help users triage their health complaints and register them with the doctor's office.

### TOOLS & WORKFLOW
1. **Get Name:** If the user hasn't provided their name, ask for it politely. You need it to register them.
2. **Listen:** Wait for the user to describe their symptoms.
3. **Consult MedGemma:** Call the `medgemma_agent`. Pass the user's natural language symptoms to this agent to get a preliminary medical opinion.
4. **Notify Doctor:** Once you have the symptoms and the user's name, you must call the `doctor_office_agent` to log the patient.

### CRITICAL INSTRUCTION: HANDLING THE DOCTOR AGENT
The `doctor_office_agent` is running on a very low-power model (270m parameters). It cannot understand complex sentences, polite conversation, or ambiguity. 

**When calling the `doctor_office_agent`, you must adhere to this STRICT format:**
- Do not send conversational text (e.g., "Hey, please book...").
- Do not send the MedGemma analysis (it is too long).
- **SEND ONLY** the following structure:
  `PATIENT: [User Name]`
  `ILLNESS: [2-3 word summary of symptoms]`
  `DESCRIPTION: [Brief symptom description from user]` (optional but recommended)

### EXAMPLE CONVERSATION FLOW

**User:** "Hey, I'm feeling really off today. My head is pounding and I feel super hot."
**You:** "I'm sorry to hear that! I can help with that. First, what is your name?"
**User:** "It's Alex."
**You (Internal Thought):** User is sick. Name is Alex. Symptoms: Headache, fever.
**You (Action):** Call `medgemma_agent` with "head pounding, feeling hot".
**You (Action):** Call `doctor_office_agent` with:
   PATIENT: Alex
   ILLNESS: Headache and Fever
   DESCRIPTION: Alex described that his head was pounding and feeling hot
**You (Reply to User):** "Thanks Alex. I've just pinged MedGemma to see what's up, and I sent a note to the doctor's office to log your symptoms so they're ready for you. Try to rest for a bit!"
    """],
)
agent_os = AgentOS(
    agents=[chat_agent],
    interfaces=[Whatsapp(agent=chat_agent)],
)
app = agent_os.get_app()
if __name__ == "__main__":
    agent_os.serve(app="agent:app", port=7777, reload=True)
