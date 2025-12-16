# student sys

A lightweight Python-based student management system. This repository provides a simple app to manage students, notes, reports, and basic data storage. Use `app.py` to start the application.

**Note:** This README is based on the current project layout. If your app requires additional configuration (database credentials, environment variables, or a specific Python version), add them in the `DB/` or project-specific docs.

**Project Overview**
- **Purpose:** Manage students, absence notes, reports and related functionality.
- **Entry point:** `app.py` — starts the application.

**Requirements**
- **Python:** 3.8+ recommended (confirm with your environment).
- **Dependencies:** See `requirements.txt` for third-party packages.

**Quick Start**
- **Create a virtual environment**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- **Install dependencies**:

```bash
pip install -r requirements.txt
```

- **Run the app**:

```bash
python3 app.py
```

If the app is a GUI, it should open a window. If it's a CLI or web app, follow prompts or check the console for a local server address.

**Project Structure**
- `app.py`: Application entry point.
- `requirements.txt`: Python package dependencies.
- `DB/`
  - `db_manager.py`: Database helper / persistence logic.
- `pages/`: UI pages and application modules (for example `home.py`, `students.py`, `add.py`, `modify.py`, `remove.py`, `report_generator.py`, etc.).
- `reports/`: Generated reports and exports.
- `Icons/`, `Images/`: Static assets used by the UI.

**Usage / Features (based on files)**
- **Manage students:** Add, modify, remove student records (`pages/students.py`, `pages/add.py`, `pages/modify.py`, `pages/remove.py`).
- **Notes & Absences:** Create and manage notes and absence records (`pages/notes.py`, `pages/absence_notes.py`).
- **Reports:** Generate reports (`pages/report_generator.py`).
- **Authentication:** Basic login handling (`pages/log_in.py`).

**Configuration**
- If `DB/db_manager.py` expects a local database file or environment variables, update the module or provide a `.env` file (not included). Inspect `DB/db_manager.py` for required settings.
