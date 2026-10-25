class PID:
    """Controlador PID discreto con límites de salida y anti-windup."""

    def __init__(self, kp, ki, kd, dt, out_min=None, out_max=None):
        if dt <= 0:
            raise ValueError("dt debe ser mayor que 0")
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.out_min = out_min
        self.out_max = out_max
        self.reset()

    def reset(self):
        """Borra el estado interno (integral y error previo)."""
        self._integral = 0.0
        self._prev_error = None

    def update(self, setpoint, measurement):
        """Calcula la señal de control para el instante actual."""
        error = setpoint - measurement

        # Proporcional
        p = self.kp * error

        # Derivativo (en el primer paso no hay error previo)
        if self._prev_error is None:
            d = 0.0
        else:
            d = self.kd * (error - self._prev_error) / self.dt
        self._prev_error = error

        # Integral tentativa
        integral = self._integral + error * self.dt
        u = p + self.ki * integral + d

        # Saturación + anti-windup por integración condicional:
        # si la salida se satura, no se acumula la integral.
        if self.out_min is not None and u < self.out_min:
            u = self.out_min
        elif self.out_max is not None and u > self.out_max:
            u = self.out_max
        else:
            self._integral = integral

        return u
