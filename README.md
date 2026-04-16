# 1st-lab

This repository contains the SecureLab prototype application.
It includes the full backend and frontend scaffold for the prototype platform,
with challenge, vulnerability, and lab pages.

## Features
- Flask backend with route handling for challenges, vulnerabilities, and labs
- Frontend templates with navigation and styled UI
- In-memory prototype data for rapid testing
- Separate repository from the main SecureLab application

## Run locally
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Then open `http://127.0.0.1:6000`.
