@echo off
setlocal
cd /d "%~dp0"

if not exist "api\.venv\Scripts\python.exe" (
  echo [ERROR] Missing api\.venv. Create it first:
  echo python -m venv api\.venv
  echo api\.venv\Scripts\python.exe -m pip install -r api\requirements-modern.txt
  exit /b 1
)

api\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir api --host 0.0.0.0 --port 8100 --reload
