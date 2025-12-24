# MedGemma Medical Advisor Agent

A medical advisor powered by an Ollama-served model, providing preliminary guidance based on symptoms. Exposes an AgentOS app for A2A communication.

## Prerequisites
- Python 3.10+
- Ollama installed and running
  - Model: `hf.co/unsloth/medgemma-4b-it-GGUF:Q2_K_XL`

## Setup
```bash
ollama pull hf.co/unsloth/medgemma-4b-it-GGUF:Q2_K_XL
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```bash
python medgemma.py
```
- Default port: 7778

## About the Model: MedGemma 🩺
This agent uses **MedGemma** (specifically the `4b` version), a specialized model from Google built on Gemma 3, optimized for medical text and image comprehension. It's designed to help developers build healthcare-focused AI applications, capable of tasks like medical image interpretation and clinical reasoning.

Check out the details here:
- [MedGemma Overview](https://deepmind.google/models/gemma/medgemma/)
- [Developer Docs](https://developers.google.com/health-ai-developer-foundations/medgemma)
- [Hugging Face Model Card](https://huggingface.co/google/medgemma-4b-it)

## Notes
- This service is intended to be queried by other agents (e.g., the WhatsApp agent) via A2A.
- I used a low quantized model due to my limited compute; you can find more accurate ones [here](https://huggingface.co/unsloth/medgemma-4b-it-GGUF).