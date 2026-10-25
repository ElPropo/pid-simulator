import pytest

from app.pid import PID
from app.plant import FirstOrderPlant


def test_proporcional():
    pid = PID(kp=2, ki=0, kd=0, dt=0.1)
    assert pid.update(setpoint=5, measurement=0) == pytest.approx(10)


def test_integral_acumula_en_el_tiempo():
    pid = PID(kp=0, ki=1, kd=0, dt=0.1)
    assert pid.update(1, 0) == pytest.approx(0.1)
    assert pid.update(1, 0) == pytest.approx(0.2)


def test_derivativo_responde_al_cambio_de_error():
    pid = PID(kp=0, ki=0, kd=1, dt=0.1)
    assert pid.update(1, 0) == pytest.approx(0)   # primer paso, sin error previo
    assert pid.update(2, 0) == pytest.approx(10)  # (2 - 1) / 0.1


def test_saturacion_limita_la_salida():
    pid = PID(kp=1, ki=0, kd=0, dt=0.1, out_min=-10, out_max=10)
    assert pid.update(100, 0) == 10
    assert pid.update(-100, 0) == -10


def test_anti_windup_no_acumula_integral_saturada():
    pid = PID(kp=1, ki=1, kd=0, dt=0.1, out_max=10)
    pid.update(100, 0)  # saturado: la integral no debe crecer
    assert pid.update(0, 0) == pytest.approx(0)


def test_reset_borra_el_estado():
    pid = PID(kp=0, ki=1, kd=0, dt=0.1)
    pid.update(1, 0)
    pid.reset()
    assert pid.update(1, 0) == pytest.approx(0.1)


def test_dt_invalido():
    with pytest.raises(ValueError):
        PID(kp=1, ki=0, kd=0, dt=0)


def test_planta_converge_a_su_ganancia():
    plant = FirstOrderPlant(gain=2, tau=1, dt=0.01)
    y = 0
    for _ in range(1000):  # 10 s con entrada constante u = 1
        y = plant.step(1)
    assert y == pytest.approx(2, abs=1e-2)


def test_pi_elimina_el_error_en_regimen_permanente():
    dt = 0.01
    pid = PID(kp=2, ki=1, kd=0, dt=dt)
    plant = FirstOrderPlant(gain=1, tau=1, dt=dt)
    y = plant.y
    for _ in range(3000):  # 30 s de simulación
        u = pid.update(1.0, y)
        y = plant.step(u)
    assert y == pytest.approx(1.0, abs=1e-2)
