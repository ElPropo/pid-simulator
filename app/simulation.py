import math

from app.metrics import compute_metrics
from app.pid import PID
from app.plant import FirstOrderPlant


def simulate(
    kp,
    ki,
    kd,
    setpoint=1.0,
    duration=20.0,
    dt=0.01,
    gain=1.0,
    tau=1.0,
    out_min=None,
    out_max=None,
):
    """Simula el lazo cerrado PID + planta ante un escalón de setpoint."""
    if tau < dt:
        raise ValueError("tau debe ser mayor o igual que dt")

    steps = int(round(duration / dt))
    pid = PID(kp, ki, kd, dt, out_min, out_max)
    plant = FirstOrderPlant(gain, tau, dt)

    t, y, u = [], [], []
    yk = plant.y
    for k in range(steps):
        uk = pid.update(setpoint, yk)
        yk = plant.step(uk)
        if not math.isfinite(yk):
            raise ValueError("La simulación divergió; revisa las ganancias")
        t.append(round((k + 1) * dt, 6))
        y.append(yk)
        u.append(uk)

    return {
        "t": t,
        "y": y,
        "u": u,
        "setpoint": setpoint,
        "metrics": compute_metrics(t, y, setpoint),
    }
