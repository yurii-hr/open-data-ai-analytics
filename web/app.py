from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import uvicorn

app = FastAPI(title="Lviv Transit Analytics Web Server")

reports_dir = "/app/shared_reports"
os.makedirs(reports_dir, exist_ok=True)

app.mount("/reports", StaticFiles(directory=reports_dir, html=True), name="reports")

@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <title>Аналітика зупинок</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: #e9ecef; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .card { background: white; padding: 50px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); max-width: 600px; text-align: center; }
            h1 { color: #2c3e50; margin-bottom: 20px;}
            p { color: #555; line-height: 1.6; font-size: 16px; margin-bottom: 30px;}
            .btn { display: inline-block; padding: 14px 28px; background: #007bff; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; transition: background 0.3s; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Транспортна система Львова</h1>
            <a href="/reports/index.html" class="btn">Переглянути результати та візуалізації</a>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":

    port = int(os.getenv("WEB_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)