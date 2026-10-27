# MediTrack Dashboard (Streamlit + MySQL)

Beginner-friendly dashboard for the existing MediTrack database. The app is read-only: it does not insert, update, or delete database records.

## 1. Requirements
- Python 3.10 or newer
- MySQL Server running
- Existing `MediTrack` database and its tables

## 2. Open the project
Extract this folder somewhere easy to find, for example:
`C:\Users\<your-user>\Documents\MediTrack_Dashboard`

## 3. Install Python packages
Open Command Prompt in this folder and run:

```bash
python -m pip install -r requirements.txt
```

## 4. Start the dashboard

```bash
python -m streamlit run app.py
```

Streamlit will open a local browser page (usually `http://localhost:8501`).

## 5. Connect to MySQL
In the sidebar, enter:
- Host: `localhost`
- Port: `3306` (unless your MySQL uses a different port)
- Username: your MySQL username (often `root`)
- Password: your own MySQL password
- Database: `MediTrack`

Click **Connect to MediTrack**.

## Troubleshooting
- Access denied: check your MySQL username/password.
- Connection refused: check that the MySQL service is running and confirm the port in Workbench.
- Unknown database/table: check the database name and table names in Workbench.
- Missing Departments table: the app still displays the doctors table without department names.
- The app reads actual records only; it does not create sample records.
