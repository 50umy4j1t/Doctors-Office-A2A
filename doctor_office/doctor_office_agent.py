import json
import os
from datetime import datetime
from pathlib import Path
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.os import AgentOS

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

"""Doctor office agent with persistent patient registry and dashboard serving."""

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent

# --- Patient Registry File ---
# Use an absolute path so runs from any working directory still update the same file
PATIENTS_FILE = SCRIPT_DIR / "patients.json"

def load_patients():
    """Load patients from JSON file"""
    if PATIENTS_FILE.exists():
        try:
            if PATIENTS_FILE.stat().st_size == 0:
                return []
            with PATIENTS_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Reset corrupted/empty file to empty list
            save_patients([])
            return []
    return []

def save_patients(patients):
    """Save patients to JSON file"""
    with PATIENTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(patients, f, indent=2)

def register_patient(name: str, illness: str, description: str = "") -> str:
    """
    Register a patient with their name, illness, and description.
    This tool updates both the JSON registry and the HTML dashboard.
    
    Args:
        name: Patient's name
        illness: Brief illness/symptom summary
        description: Detailed description of symptoms
    
    Returns:
        Confirmation message
    """
    patients = load_patients()
    
    # Check if patient already exists
    existing = next((p for p in patients if p["name"].lower() == name.lower()), None)
    
    patient_record = {
        "name": name,
        "illness": illness,
        "description": description,
        "timestamp": datetime.now().isoformat(),
        "status": "registered"
    }
    
    if existing:
        # Update existing patient
        patients = [p if p["name"].lower() != name.lower() else patient_record for p in patients]
        message = f"Updated patient {name} with illness: {illness}"
    else:
        # Add new patient
        patients.append(patient_record)
        message = f"Registered patient {name} with illness: {illness}"
    
    save_patients(patients)
    return message

def get_patient_list() -> str:
    """
    Get the list of all registered patients.
    
    Returns:
        Formatted list of patients
    """
    patients = load_patients()
    if not patients:
        return "No patients registered yet."
    
    patient_list = "Registered Patients:\n"
    for i, p in enumerate(patients, 1):
        patient_list += f"{i}. {p['name']} - {p['illness']}\n"
    
    return patient_list

def clear_all_patients() -> str:
    """Clear all patient records from the registry."""
    save_patients([])
    return "All patient records cleared."

# --- Doctor Office Agent ---
doctor_office_agent = Agent(
    name="Doctor Office Assistant",
    id="doctor_office_agent",
    model=Ollama(id="functiongemma:270m"),debug_mode=True,
    tools=[register_patient, get_patient_list, clear_all_patients],
    markdown=True,
    description="You are a doctor office assistant that registers and manages patient records.",
    instructions=["""### SIMPLE INSTRUCTIONS FOR DOCTOR OFFICE
You are a small office assistant. Your job is VERY SIMPLE.

### WHAT YOU DO
1. READ: You will receive a message with PATIENT name and ILLNESS
2. REGISTER: Use the register_patient tool to save the patient
3. CONFIRM: Tell the user the patient is registered

### MESSAGE FORMAT YOU WILL RECEIVE
The message will look like:
PATIENT: [NAME]
ILLNESS: [SYMPTOMS]
DESCRIPTION: [DESCRIPTION]

### YOUR ONLY JOB
- Extract the PATIENT name
- Extract the ILLNESS
- Extract the DESCRIPTION (if present)
- Call register_patient with these pieces of information
- That's it. Nothing more.

### DO NOT
- Ask questions
- Have conversations
- Change the information you receive
- Do anything except register the patient

### EXAMPLE
Message in: 
PATIENT: John Smith
ILLNESS: Headache and Fever
DESCRIPTION: Persistent headache for 2 hours, high fever

Action: Call register_patient(name="John Smith", illness="Headache and Fever", description="Persistent headache for 2 hours, high fever")
Response: Confirm the patient was registered
    """],
)

agent_os = AgentOS(
    agents=[doctor_office_agent],
    a2a_interface=True
)

app = agent_os.get_app()

# Mount static files from the script directory
app.mount("/static", StaticFiles(directory=str(SCRIPT_DIR)), name="static")

@app.get("/")
async def root():
    """Serve the patients dashboard HTML"""
    return FileResponse(str(SCRIPT_DIR / "index.html"))

@app.get("/patientspage")
async def read_index():
    """Alternative route for patients page"""
    return FileResponse(str(SCRIPT_DIR / "index.html"))
if __name__ == "__main__":
    load_patients()
    agent_os.serve(app="doctor_office_agent:app", port=7779, host="0.0.0.0", reload=True)
