def compute_metrics(t, y, setpoint, band=0.02):
    """Métricas de la respuesta a un escalón (setpoint > 0)."""
    # Sobreimpulso en porcentaje respecto al setpoint
    overshoot = max(0.0, (max(y) - setpoint) / setpoint * 100)

    # Tiempo de establecimiento: primer instante desde el cual la salida
    # queda dentro de la banda (por defecto ±2 %) hasta el final.
    tol = band * setpoint
    last_outside = None
    for i, yi in enumerate(y):
        if abs(yi - setpoint) > tol:
            last_outside = i

    if last_outside is None:
        settling_time = 0.0
    elif last_outside == len(y) - 1:
        settling_time = None  # nunca se estabilizó dentro de la simulación
    else:
        settling_time = t[last_outside + 1]

    return {
        "overshoot_pct": overshoot,
        "settling_time": settling_time,
        "steady_state_error": setpoint - y[-1],
    }
