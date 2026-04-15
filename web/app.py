from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
import uvicorn

app = FastAPI(title="Lviv Transit Analytics Web Server")

reports_dir = "/app/shared_reports"
os.makedirs(reports_dir, exist_ok=True)

app.mount("/reports", StaticFiles(directory=reports_dir, html=True), name="reports")

@app.get("/")
def root():
    return RedirectResponse(url="/reports/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)