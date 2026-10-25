import pytest

from app.simulation import simulate


def test_pi_converge_sin_error_ni_sobreimpulso():
    r = simulate(kp=2, ki=1, kd=0, duration=30)
    m = r["metrics"]
    assert m["steady_state_error"] == pytest.approx(0, abs=1e-2)
    assert m["overshoot_pct"] == pytest.approx(0, abs=1)
    assert m["settling_time"] is not None


def test_solo_proporcional_deja_error_permanente():
    r = simulate(kp=1, ki=0, kd=0, duration=20)
    m = r["metrics"]
    assert m["steady_state_error"] == pytest.approx(0.5, abs=1e-2)
    assert m["settling_time"] is None


def test_simulacion_divergente_lanza_error():
    with pytest.raises(ValueError):
        simulate(kp=1000, ki=0, kd=0, dt=0.1, duration=20)


def test_tau_menor_que_dt_lanza_error():
    with pytest.raises(ValueError):
        simulate(kp=1, ki=0, kd=0, dt=0.1, tau=0.05)
