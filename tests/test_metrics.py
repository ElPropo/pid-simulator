import pytest

from app.metrics import compute_metrics


def test_sobreimpulso_y_tiempo_de_establecimiento():
    t = [1, 2, 3, 4, 5]
    y = [0.5, 1.2, 1.01, 1.0, 1.0]
    m = compute_metrics(t, y, setpoint=1.0)
    assert m["overshoot_pct"] == pytest.approx(20)
    assert m["settling_time"] == 3
    assert m["steady_state_error"] == pytest.approx(0)


def test_sin_sobreimpulso():
    m = compute_metrics([1, 2, 3, 4], [0.5, 0.9, 0.99, 1.0], setpoint=1.0)
    assert m["overshoot_pct"] == 0


def test_nunca_se_estabiliza():
    m = compute_metrics([1, 2, 3], [0.5, 0.6, 0.7], setpoint=1.0)
    assert m["settling_time"] is None
