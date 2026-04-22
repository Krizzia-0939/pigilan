# Pigilan

Pigilan is a Streamlit-based ASF monitoring app for pig farmers and field users. It is built around a simple workflow: check the pig, save the report locally, and sync later when internet is available.

Main things it can do:

- create local farmer accounts
- assess pigs for possible ASF risk
- upload a pig image for model-based screening
- save reports locally in SQLite
- review nearby case alerts
- track farm biosecurity
- export or sync records later when internet is available

This project is currently built for a local-first workflow using:

- Frontend: Streamlit
- Backend: Python
- Database: SQLite
- ML Model: Teachable Machine export stored in `models/`
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

- The app is local-first for the core farmer workflow, but it still runs through Streamlit.
- On local development, the Streamlit server must be running for the app to open in the browser.
- The map background uses online tiles, so map tiles may be blank without internet.
- GPS and manual coordinates can still be used even if map tiles do not load.
- The PWA support is limited because this is still a Streamlit app, not a native mobile app.

## Folder Guide

Main files your teammates should know:

- [`app.py`](/c:/Users/jacer/Downloads/New/pigilan/app.py)
  Main Streamlit entry file. Handles top navigation and loads the page views.

- [`core/`](/c:/Users/jacer/Downloads/New/pigilan/core)
  Core application logic:
  `backend.py`, `database.py`, `pdf_utils.py`

- [`shared/`](/c:/Users/jacer/Downloads/New/pigilan/shared)
  Shared helpers for assets, PWA injection, and location picking.

- [`ml/`](/c:/Users/jacer/Downloads/New/pigilan/ml)
  ML runtime code:
  `ml_model.py`, `ml_model_compat.py`, `ml_compat_runner.py`

- [`models/`](/c:/Users/jacer/Downloads/New/pigilan/models)
  Model assets:
  `keras_model.h5`, `compat_model.keras`, `labels.txt`

- [`components/streamlit_js_eval/`](/c:/Users/jacer/Downloads/New/pigilan/components/streamlit_js_eval)
  Custom Streamlit component used for browser geolocation.

- [`sync_server.py`](/c:/Users/jacer/Downloads/New/pigilan/sync_server.py)
  Sync server entry point.

- [`requirements.txt`](/c:/Users/jacer/Downloads/New/pigilan/requirements.txt)
  Python dependencies.

- [`pigilan.db`](/c:/Users/jacer/Downloads/New/pigilan/pigilan.db)
  Local SQLite database file.

- [`views/`](/c:/Users/jacer/Downloads/New/pigilan/views)
  Streamlit page files:
  `home.py`, `about.py`, `asf_detection.py`, `cases.py`, `account.py`, `biosecurity.py`

- [`assets/`](/c:/Users/jacer/Downloads/New/pigilan/assets)
  Local images used by the UI.

- [`static/`](/c:/Users/jacer/Downloads/New/pigilan/static)
  PWA-related files like manifest, icon, and service worker.

- [`.streamlit/config.toml`](/c:/Users/jacer/Downloads/New/pigilan/.streamlit/config.toml)
  Enables static serving for PWA assets.

## Setup Requirements

Recommended Python version:

- Python `3.11`

Avoid newer unsupported runtimes for this repo. The TensorFlow stack in `requirements.txt` is aligned to Python `3.11`.

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

If you prefer the batch file launcher, you can also double-click [`run_app.bat`](/c:/Users/jacer/Downloads/New/pigilan/run_app.bat). It now checks for a usable Python runtime and tells you what is missing instead of failing silently.

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

- [`app.py`](/c:/Users/jacer/Downloads/New/pigilan/app.py)
- [`views/home.py`](/c:/Users/jacer/Downloads/New/pigilan/views/home.py)
- [`views/asf_detection.py`](/c:/Users/jacer/Downloads/New/pigilan/views/asf_detection.py)
- [`views/cases.py`](/c:/Users/jacer/Downloads/New/pigilan/views/cases.py)
- [`views/account.py`](/c:/Users/jacer/Downloads/New/pigilan/views/account.py)

If they are changing backend/database behavior, they should review:

- [`core/backend.py`](/c:/Users/jacer/Downloads/New/pigilan/core/backend.py)
- [`core/database.py`](/c:/Users/jacer/Downloads/New/pigilan/core/database.py)
- [`sync_server.py`](/c:/Users/jacer/Downloads/New/pigilan/sync_server.py)

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

### 6. Double-clicking `run_app.bat` does nothing

Usually means there is no working Python runtime on the machine yet, or `streamlit` is not installed in the selected runtime.

Fix:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Files That Can Usually Be Ignored In Handoff

- `.venv/`
- `__pycache__/`

## Suggested Team Handoff Package

Share the whole project except `.venv` if you want a lighter handoff:

- `app.py`
- `core/`
- `shared/`
- `ml/`
- `models/`
- `components/`
- `sync_server.py`
- `requirements.txt`
- `README.md`
- `pigilan.db`
- `views/`
- `assets/`
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
