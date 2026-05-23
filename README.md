# Pigilan is a Streamlit-based ASF monitoring system for pig farmers. It helps users:

- create local farmer accounts
- check pigs for possible ASF risk
- upload a pig image for ML-based detection
- save cases locally
- view nearby case alerts
- track farm biosecurity
- export or sync records later when internet is available

This project is currently built for a local-first workflow using:

- Frontend: Streamlit
- Backend: Python
- Database: SQLite
- ML Model: Teachable Machine export (`keras_model.h5`)
- Sync Server: FastAPI

## Current App Flow

For farmers:

- `Home`
- `Check Pig`
- `Cases`
- `Account`

For admin:

- `Dashboard`

Main working features right now:

- local sign up and sign in
- ASF risk assessment from symptoms
- image-based ASF detection
- nearby case alerts
- saved case history
- PDF case export
- biosecurity checklist
- local-first saving in SQLite
- basic push sync with a sync server

## Important Notes

- The app is offline-first for the core farmer workflow, but it still runs through Streamlit.
- On local development, the Streamlit server must be running for the app to open.
- The map background uses online tiles, so map tiles may be blank without internet.
- GPS and manual coordinates can still be used even if map tiles do not load.
- The PWA support is basic/best-effort because this is still a Streamlit app.

## Folder Guide

Main files your teammates should know:

- [`app.py`](/c:/Users/jacer/Downloads/pigilan/app.py)
  Main Streamlit entry file. Handles top navigation and loads the page views.

- [`backend.py`](/c:/Users/jacer/Downloads/pigilan/backend.py)
  Main application logic. Includes:
  local account handling, case saving, risk assessment, alerts, PDF export, and push sync.

- [`database.py`](/c:/Users/jacer/Downloads/pigilan/database.py)
  SQLite schema and database functions.

- [`ml_model.py`](/c:/Users/jacer/Downloads/pigilan/ml_model.py)
  Loads the Teachable Machine model and runs image prediction.

- [`location_picker.py`](/c:/Users/jacer/Downloads/pigilan/location_picker.py)
  GPS, map click, and manual coordinate entry logic.

- [`pdf_utils.py`](/c:/Users/jacer/Downloads/pigilan/pdf_utils.py)
  PDF report generation helpers.

- [`sync_server.py`](/c:/Users/jacer/Downloads/pigilan/sync_server.py)
  FastAPI server for receiving sync pushes.

- [`requirements.txt`](/c:/Users/jacer/Downloads/pigilan/requirements.txt)
  Python dependencies.

- [`pigilan.db`](/c:/Users/jacer/Downloads/pigilan/pigilan.db)
  Local SQLite database file.

- [`keras_model.h5`](/c:/Users/jacer/Downloads/pigilan/keras_model.h5)
  ML model file.

- [`labels.txt`](/c:/Users/jacer/Downloads/pigilan/labels.txt)
  Class labels for the model.

- [`views/`](/c:/Users/jacer/Downloads/pigilan/views)
  Streamlit page files:
  `home.py`, `about.py`, `asf_detection.py`, `cases.py`, `account.py`, `biosecurity.py`

- [`static/`](/c:/Users/jacer/Downloads/pigilan/static)
  PWA-related files like manifest, icon, and service worker.

- [`.streamlit/config.toml`](/c:/Users/jacer/Downloads/pigilan/.streamlit/config.toml)
  Enables static serving for PWA assets.

## Setup Requirements

Recommended Python version:

- Python `3.11`

Do not use Python `3.14` for this project because some dependencies like TensorFlow/Streamlit-related packages may fail.

## First-Time Setup

Open PowerShell in the project folder:

```powershell
cd "C:\Users\jacer\Downloads\pigilan"
```

Create the virtual environment:

```powershell
py -3.11 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## How To Run The Main App

If the virtual environment is already set up:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\app.py
```

Usually the app opens at:

```text
http://localhost:8501
```

## How To Run The Sync Server

The sync server is only needed if you want `Sync` to work.

Open a second PowerShell terminal in the same project folder and run:

```powershell
python sync_server.py
```

Health check:

```text
http://127.0.0.1:8000/health
```

Expected result:

```json
{"status":"ok"}
```

## Local Development Workflow

Use two terminals:

Terminal 1:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\app.py
```

Terminal 2:

```powershell
python sync_server.py
```

## Farmer Workflow

1. Open `Account`
2. Sign up or sign in
3. Go to `Check Pig`
4. Enter symptoms, location, and image
5. Save the pig check
6. Go to `Cases` to review alerts and saved records
7. Go to `Account` for:
   sync, biosecurity checklist, backup, and profile editing

## Sync Workflow

### Push Sync

Farmer side:

1. Make sure the sync server is running
2. Open `Account`
3. Click `Sync`

Current default local sync URL:

```text
http://127.0.0.1:8000
```

## Admin Account

Default admin credentials:

- Username: `admin`
- Password: `admin123`

Change this before real deployment.

## Offline Behavior

What works offline on the same device:

- local sign up/sign in
- ASF detection
- risk assessment
- local case saving
- local biosecurity saving

What is limited offline:

- online map tiles
- push sync
- opening the app if the local Streamlit server is not running

## PWA Notes

This project includes:

- `manifest.json`
- `service-worker.js`
- app icon
- manifest/service worker injection

That means the app can be treated as a basic Streamlit-based PWA for demo/school use.

Important:

- it is still fundamentally a Streamlit web app
- if running locally, the local Streamlit server must still be running
- installable browser behavior is supported, but this is not a full native standalone app

## Deployment Notes

For a simple deployed setup:

1. deploy the Streamlit app
2. deploy the FastAPI sync server
3. set one fixed sync server URL
4. keep local-first save behavior for farmers

Once deployed, sync becomes easier because:

- the sync server can stay online 24/7
- users do not need to run local `uvicorn`
- users do not need `localhost` for sync

## Teammate Handoff Notes

If your teammates are working on frontend/design, they should mainly look at:

- [`app.py`](/c:/Users/jacer/Downloads/pigilan/app.py)
- [`views/home.py`](/c:/Users/jacer/Downloads/pigilan/views/home.py)
- [`views/asf_detection.py`](/c:/Users/jacer/Downloads/pigilan/views/asf_detection.py)
- [`views/cases.py`](/c:/Users/jacer/Downloads/pigilan/views/cases.py)
- [`views/account.py`](/c:/Users/jacer/Downloads/pigilan/views/account.py)

If they are changing backend/database behavior, they should review:

- [`backend.py`](/c:/Users/jacer/Downloads/pigilan/backend.py)
- [`database.py`](/c:/Users/jacer/Downloads/pigilan/database.py)
- [`sync_server.py`](/c:/Users/jacer/Downloads/pigilan/sync_server.py)

## Common Problems

### 1. `ModuleNotFoundError`

Usually means dependencies are not installed in the current venv.

Fix:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. `localhost refused to connect`

Usually means Streamlit is not running.

Fix:

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\app.py
```

### 3. Sync says connection refused

Usually means the sync server is not running.

Fix:

```powershell
.\.venv\Scripts\python.exe -m uvicorn sync_server:app --host 127.0.0.1 --port 8000
```

### 4. Map tiles are blank

This is expected when internet is weak or unavailable. Use:

- GPS button
- map click if visible
- manual latitude/longitude

### 5. Python version problems

Use Python `3.11` and recreate `.venv` if needed.

## Files That Can Usually Be Ignored In Handoff

- `.venv/`
- `__pycache__/`

## Suggested Team Handoff Package

Share the whole project except `.venv` if you want a lighter handoff:

- `app.py`
- `backend.py`
- `database.py`
- `location_picker.py`
- `ml_model.py`
- `pdf_utils.py`
- `sync_server.py`
- `requirements.txt`
- `README.md`
- `labels.txt`
- `keras_model.h5`
- `pigilan.db`
- `views/`
- `static/`
- `.streamlit/`

## Quick Start For Teammates

If your teammate just wants to run it fast:

```powershell
cd "C:\Users\jacer\Downloads\pigilan"
py -3.11 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

If they also want sync:

```powershell
.\.venv\Scripts\python.exe -m uvicorn sync_server:app --host 127.0.0.1 --port 8000
```
