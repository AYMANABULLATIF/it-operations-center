# IT Operations Center

IT Operations Center is a portfolio-ready Streamlit application that simulates a small internal IT operations portal for an entry-level IT Support, Helpdesk, or Desktop Support role in Japan.

The project uses mock data only. It does not connect to real Active Directory, MDM, ticketing systems, company data, or credentials. It is intentionally scoped as a realistic MVP that can be built, deployed, and explained in 1-2 days.

## Project Overview

This app demonstrates everyday IT support workflows:

- User account lookup and simulated account actions
- Device and asset assignment tracking
- Simple incident creation and status updates
- Audit logging for technician actions
- Optional Gemini-powered checklist generation
- English and Japanese UI support

Suggested positioning:

> Built a bilingual IT operations portal that simulates user account support, device asset management, incident tracking, audit logging, and AI-assisted troubleshooting workflows for a small company IT team.

## Why This Is Relevant to IT Support / Helpdesk Jobs

Helpdesk and desktop support roles often require structured troubleshooting, accurate ticket updates, asset awareness, account support, and clear documentation. This project shows those skills in a practical way without pretending to be a production identity or asset management system.

It is especially relevant for roles in Japan because the interface supports both English and professional Japanese, reflecting bilingual workplace support environments.

## Features

### Dashboard

The dashboard shows operational metrics such as:

- Total users
- Active, locked, and disabled accounts
- Total and assigned devices
- Devices in repair
- Open incidents
- High priority incidents
- Recent audit activity
- Warranty watch list

### User Management Simulator

Technicians can:

- Search users by name, email, department, or username
- View user profile and account status
- Simulate unlock account
- Simulate password reset
- Disable or enable account
- Reset MFA
- Add or remove group membership

Every action updates SQLite records and writes an audit log entry.

### Asset Management

The asset page tracks company devices with:

- Asset tag
- Hostname
- Device type
- Manufacturer and model
- Serial number
- Assigned user
- Status
- Purchase date
- Warranty expiry

Technicians can search assets, assign a device to a user, return a device to storage, mark a device as in repair, and view device history.

### Incident Tracker

The incident page supports:

- Creating incidents
- Searching incidents
- Updating status
- Updating priority
- Categorizing issues
- Linking incidents to a user and/or asset
- Recording technician notes

### Audit Log

The audit log records:

- Timestamp
- Technician name
- Action
- Target type and ID
- Details

This demonstrates the importance of traceability in IT operations.

### AI Assistant

The optional Gemini assistant can generate:

- New employee onboarding checklist
- Offboarding checklist
- Troubleshooting checklist by incident category
- Device troubleshooting checklist by asset type

If `GEMINI_API_KEY` is not configured, the app automatically uses local fallback checklists.

### Bilingual Support

The sidebar includes a language toggle:

- English
- 日本語

UI labels, buttons, page names, help text, and output messages are translated. Gemini prompts request output in the selected language.

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- python-dotenv
- Google Gemini API through `google-generativeai` (optional)

## Project Structure

```text
it_operations_center/
|-- app.py
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- README.md
|-- screenshots/
|   `-- .gitkeep
`-- sample_data/
    `-- .gitkeep
```

The SQLite database is created automatically on first run and seeded with realistic mock users, assets, incidents, audit logs, and device history.

## How To Run Locally On Windows

From PowerShell:

```powershell
cd "C:\path\to\IT HELP DESK\it_operations_center"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

Gemini is optional. The app works without an API key.

## Gemini API Setup

For local development, copy `.env.example` to `.env` and set:

```text
GEMINI_API_KEY=your_key_here
```

Do not commit `.env`.

For Streamlit Community Cloud, add this secret in the app settings:

```toml
GEMINI_API_KEY = "your_key_here"
```

If the secret is missing, the app displays local fallback checklists.

## Deploy On Streamlit Community Cloud

1. Push this project to GitHub.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Create a new app from the GitHub repository.
4. Set the main file path to:

```text
it_operations_center/app.py
```

5. Confirm `requirements.txt` is available in the same folder or configure the repository so Streamlit installs the dependencies.
6. Add `GEMINI_API_KEY` in Streamlit secrets only if you want AI-generated checklists.
7. Deploy the app.

Note: SQLite data on Streamlit Community Cloud is suitable for demo use only. It may reset when the app restarts or redeploys.

## Example Use Cases

- A user is locked out after entering the wrong password several times. The technician searches the user, verifies status, unlocks the account, and records the action automatically in the audit log.
- A laptop is returned by a former employee. The technician marks the device as storage and checks the device history.
- A printer issue is reported. The technician creates a hardware incident, links it to the printer asset, changes the status to In Progress, and adds notes.
- A new employee joins the Sales department. The technician uses the AI assistant or fallback checklist to prepare onboarding steps.

## Resume Bullet Points

- Built a bilingual Streamlit IT operations portal that simulates user account support, asset management, incident tracking, and audit logging using Python, SQLite, and Pandas.
- Implemented realistic helpdesk workflows including account unlock, password reset simulation, MFA reset, device assignment, incident updates, and technician activity history.
- Added optional Gemini-powered checklist generation with local fallback logic, allowing the app to run safely without real credentials or production system access.

## Interview Explanation

This project represents a small internal tool that an IT support team might use to organize daily support work. It is not connected to real company systems, but it models the logic and documentation habits expected in helpdesk operations.

In an interview, you can explain:

- The database design separates users, assets, incidents, audit logs, and device history.
- All support actions create an audit log so technician work is traceable.
- The app avoids real credentials and production integrations, making it safe for a portfolio demo.
- The bilingual interface reflects the needs of international workplaces in Japan.
- Gemini is optional, and the app remains deployable even when no API key is configured.

## Future Improvements

- Add CSV import/export for users, assets, and incidents.
- Add role-based technician views.
- Add charts for incident resolution time.
- Add warranty expiry alerts.
- Add more detailed Japanese support templates.
- Replace mock actions with real integrations only in a controlled lab environment.
