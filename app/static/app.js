const groups = {
  "controller-controls": [
    { id: "kp", label: "Kp (proporcional)", min: 0, max: 20, step: 0.1, value: 2 },
    { id: "ki", label: "Ki (integral)", min: 0, max: 10, step: 0.1, value: 1 },
    { id: "kd", label: "Kd (derivativo)", min: 0, max: 5, step: 0.05, value: 0 },
    { id: "setpoint", label: "Setpoint", min: 0.1, max: 10, step: 0.1, value: 1 },
  ],
  "plant-controls": [
    { id: "gain", label: "Ganancia de la planta (K)", min: 0.1, max: 5, step: 0.1, value: 1 },
    { id: "tau", label: "Constante de tiempo τ (s)", min: 0.1, max: 10, step: 0.1, value: 1 },
    { id: "duration", label: "Duración (s)", min: 5, max: 60, step: 1, value: 20 },
  ],
};

const state = {};
const inputs = {};

function buildControls() {
  for (const [containerId, items] of Object.entries(groups)) {
    const container = document.getElementById(containerId);
    for (const c of items) {
      state[c.id] = c.value;

      const wrap = document.createElement("div");
      wrap.className = "control";
      wrap.innerHTML = `
        <label for="${c.id}">${c.label}: <output>${c.value}</output></label>
        <input type="range" id="${c.id}" min="${c.min}" max="${c.max}" step="${c.step}" value="${c.value}">
      `;
      container.appendChild(wrap);

      const input = wrap.querySelector("input");
      const output = wrap.querySelector("output");
      inputs[c.id] = { input, output, def: c.value };

      input.addEventListener("input", () => {
        state[c.id] = parseFloat(input.value);
        output.textContent = input.value;
        scheduleSimulation();
      });
    }
  }
}

// ---------- Gráficos ----------
Chart.defaults.color = getComputedStyle(document.body).color;
Chart.defaults.borderColor = "rgba(128, 128, 128, 0.25)";

function makeChart(canvasId, yTitle, datasets, showLegend) {
  return new Chart(document.getElementById(canvasId), {
    type: "line",
    data: { datasets },
    options: {
      animation: false,
      responsive: true,
      maintainAspectRatio: false,
      elements: { point: { radius: 0 }, line: { borderWidth: 2 } },
      scales: {
        x: { type: "linear", title: { display: true, text: "Tiempo (s)" } },
        y: { title: { display: true, text: yTitle } },
      },
      plugins: { legend: { display: showLegend } },
    },
  });
}

const chartY = makeChart(
  "chart-y",
  "Salida",
  [
    { label: "Salida y(t)", data: [], borderColor: "#2f6fed" },
    { label: "Setpoint", data: [], borderColor: "#8a8f99", borderDash: [6, 6] },
  ],
  true
);

const chartU = makeChart(
  "chart-u",
  "Señal de control",
  [{ label: "Control u(t)", data: [], borderColor: "#e8833a" }],
  false
);

const toPoints = (t, v) => t.map((x, i) => ({ x, y: v[i] }));

function updateCharts(d) {
  const last = d.t[d.t.length - 1];
  chartY.data.datasets[0].data = toPoints(d.t, d.y);
  chartY.data.datasets[1].data = [
    { x: 0, y: d.setpoint },
    { x: last, y: d.setpoint },
  ];
  chartU.data.datasets[0].data = toPoints(d.t, d.u);
  chartY.update("none");
  chartU.update("none");
}

// ---------- Métricas y errores ----------
function updateMetrics(m) {
  document.getElementById("m-overshoot").textContent = `${m.overshoot_pct.toFixed(1)} %`;
  document.getElementById("m-settling").textContent =
    m.settling_time === null ? "No se estabiliza" : `${m.settling_time.toFixed(2)} s`;
  document.getElementById("m-error").textContent = m.steady_state_error.toFixed(3);
}

function showError(msg) {
  const el = document.getElementById("error");
  el.textContent = msg;
  el.hidden = false;
}

function hideError() {
  document.getElementById("error").hidden = true;
}

// ---------- Simulación ----------
let timer = null;
let requestId = 0;

function scheduleSimulation() {
  clearTimeout(timer);
  timer = setTimeout(runSimulation, 150);
}

async function runSimulation() {
  const id = ++requestId;
  try {
    const res = await fetch("/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state),
    });
    const data = await res.json();
    if (id !== requestId) return; // llegó una respuesta más nueva

    if (!res.ok) {
      showError(typeof data.detail === "string" ? data.detail : "Parámetros inválidos");
      return;
    }
    hideError();
    updateCharts(data);
    updateMetrics(data.metrics);
  } catch (err) {
    showError("No se pudo conectar con el servidor");
  }
}

document.getElementById("reset").addEventListener("click", () => {
  for (const [id, { input, output, def }] of Object.entries(inputs)) {
    input.value = def;
    output.textContent = def;
    state[id] = def;
  }
  runSimulation();
});

buildControls();
runSimulation();
