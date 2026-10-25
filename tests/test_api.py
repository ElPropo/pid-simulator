from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_simulate_devuelve_series_y_metricas():
    r = client.post("/simulate", json={"kp": 2, "ki": 1, "kd": 0, "duration": 10})
    assert r.status_code == 200
    data = r.json()
    assert len(data["t"]) == len(data["y"]) == len(data["u"]) == 1000
    assert set(data["metrics"]) == {
        "overshoot_pct",
        "settling_time",
        "steady_state_error",
    }


def test_simulate_rechaza_parametros_invalidos():
    r = client.post("/simulate", json={"kp": -1})
    assert r.status_code == 422


def test_simulate_divergente_devuelve_422():
    r = client.post(
        "/simulate",
        json={"kp": 1000, "ki": 0, "kd": 0, "dt": 0.1, "duration": 20},
    )
    assert r.status_code == 422
