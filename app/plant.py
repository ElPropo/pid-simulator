class FirstOrderPlant:
    """Planta de primer orden: tau * dy/dt = -y + gain * u."""

    def __init__(self, gain, tau, dt, y0=0.0):
        if tau <= 0 or dt <= 0:
            raise ValueError("tau y dt deben ser mayores que 0")
        self.gain = gain
        self.tau = tau
        self.dt = dt
        self.y = y0

    def step(self, u):
        """Avanza un paso de simulación y devuelve la nueva salida."""
        self.y += self.dt / self.tau * (-self.y + self.gain * u)
        return self.y
