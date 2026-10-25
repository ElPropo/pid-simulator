from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.simulation import simulate

app = FastAPI(title="Simulador PID")


class SimulationRequest(BaseModel):
    kp: float = Field(2.0, ge=0)
    ki: float = Field(1.0, ge=0)
    kd: float = Field(0.0, ge=0)
    setpoint: float = Field(1.0, gt=0)
    duration: float = Field(20.0, gt=0, le=100)
    dt: float = Field(0.01, ge=0.005, le=0.1)
    gain: float = 1.0
    tau: float = Field(1.0, gt=0)
    out_min: float | None = None
    out_max: float | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/simulate")
def run_simulation(params: SimulationRequest):
    try:
        return simulate(**params.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
