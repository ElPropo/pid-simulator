from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Simulador PID")


@app.get("/health")
def health():
    return {"status": "ok"}


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
