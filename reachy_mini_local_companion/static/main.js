// === Antenna Controls ===
let antennasEnabled = true;

async function updateAntennasState(enabled) {
    try {
        const resp = await fetch("/antennas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ enabled }),
        });
        const data = await resp.json();
        antennasEnabled = data.antennas_enabled;
        updateAntennaUI();
    } catch (e) {
        document.getElementById("status").textContent = "Backend error";
    }
}

async function playSound() {
    try {
        await fetch("/play_sound", { method: "POST" });
    } catch (e) {
        console.error("Error triggering sound:", e);
    }
}

function updateAntennaUI() {
    const checkbox = document.getElementById("antenna-checkbox");
    const status = document.getElementById("status");

    checkbox.checked = antennasEnabled;

    if (antennasEnabled) {
        status.textContent = "Antennas status: running";
    } else {
        status.textContent = "Antennas status: stopped";
    }
}

document.getElementById("antenna-checkbox").addEventListener("change", (e) => {
    updateAntennasState(e.target.checked);
});

document.getElementById("sound-btn").addEventListener("click", () => {
    playSound();
});

updateAntennaUI();

// === Speech-to-Text Controls ===
let sttEnabled = false;
let sttState = "idle";
let pollingInterval = null;

async function fetchSTTStatus() {
    try {
        const resp = await fetch("/stt/status");
        const data = await resp.json();
        updateSTTStatusUI(data);
        return data;
    } catch (e) {
        console.error("Error fetching STT status:", e);
        return null;
    }
}

async function updateSTTConfig(config) {
    try {
        const resp = await fetch("/stt/config", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(config),
        });
        const data = await resp.json();
        if (data.status === "error") {
            showSTTError(data.error);
        } else {
            await fetchSTTStatus();
        }
        return data;
    } catch (e) {
        console.error("Error updating STT config:", e);
        showSTTError("Failed to update configuration");
        return null;
    }
}

async function fetchTranscripts() {
    try {
        const resp = await fetch("/stt/transcripts");
        const transcripts = await resp.json();
        updateTranscriptList(transcripts);
    } catch (e) {
        console.error("Error fetching transcripts:", e);
    }
}

async function startListening() {
    try {
        await fetch("/stt/listen/start", { method: "POST" });
        await fetchSTTStatus();
    } catch (e) {
        console.error("Error starting listening:", e);
    }
}

async function stopListening() {
    try {
        await fetch("/stt/listen/stop", { method: "POST" });
        await fetchSTTStatus();
    } catch (e) {
        console.error("Error stopping listening:", e);
    }
}

async function clearTranscripts() {
    try {
        await fetch("/stt/transcripts", { method: "DELETE" });
        updateTranscriptList([]);
    } catch (e) {
        console.error("Error clearing transcripts:", e);
    }
}

function updateSTTStatusUI(status) {
    sttEnabled = status.enabled;
    sttState = status.state;

    // Update enabled checkbox
    document.getElementById("stt-enabled").checked = status.enabled;

    // Update state indicator
    const stateEl = document.getElementById("stt-state");
    stateEl.className = `stt-state ${status.state}`;
    const stateTextEl = stateEl.querySelector(".state-text");
    const stateMap = {
        idle: "Idle",
        wake_detected: "Wake Detected",
        listening: "Listening...",
        processing: "Processing...",
    };
    stateTextEl.textContent = stateMap[status.state] || status.state;

    // Update model status
    const modelStatus = document.getElementById("stt-model-status");
    if (status.model_loaded) {
        modelStatus.textContent = `Model: ${status.engine} (loaded)`;
        modelStatus.className = "loaded";
    } else if (status.enabled) {
        modelStatus.textContent = "Model: Loading...";
        modelStatus.className = "loading";
    } else {
        modelStatus.textContent = "Model: Not loaded";
        modelStatus.className = "";
    }

    // Update button states
    const listenBtn = document.getElementById("stt-listen-btn");
    const stopBtn = document.getElementById("stt-stop-btn");

    listenBtn.disabled = !status.model_loaded || status.state !== "idle";
    stopBtn.disabled = !status.model_loaded || status.state === "idle";

    // Show error if present
    if (status.error) {
        showSTTError(status.error);
    }
}

function updateTranscriptList(transcripts) {
    const listEl = document.getElementById("transcript-list");

    if (transcripts.length === 0) {
        listEl.innerHTML =
            '<p class="placeholder">No transcripts yet. Enable STT and speak to see results.</p>';
        return;
    }

    listEl.innerHTML = transcripts
        .slice()
        .reverse()
        .map((t) => {
            const time = new Date(t.timestamp * 1000).toLocaleTimeString();
            const wakeWord = t.wake_word ? `<span class="wake-word">${t.wake_word}</span>` : "";
            return `
            <div class="transcript-item">
                <span class="transcript-time">${time}</span>
                ${wakeWord}
                <span class="transcript-text">${escapeHtml(t.text)}</span>
            </div>
        `;
        })
        .join("");
}

function showSTTError(message) {
    const modelStatus = document.getElementById("stt-model-status");
    modelStatus.textContent = `Error: ${message}`;
    modelStatus.className = "error";
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function startPolling() {
    if (pollingInterval) return;
    pollingInterval = setInterval(async () => {
        await fetchSTTStatus();
        if (sttEnabled) {
            await fetchTranscripts();
        }
    }, 1000);
}

function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}

// STT Event Listeners
document.getElementById("stt-enabled").addEventListener("change", async (e) => {
    await updateSTTConfig({ enabled: e.target.checked });
    if (e.target.checked) {
        startPolling();
    }
});

document.getElementById("stt-engine").addEventListener("change", async (e) => {
    await updateSTTConfig({ engine: e.target.value });
});

document.getElementById("stt-wake-word").addEventListener("change", async (e) => {
    await updateSTTConfig({ wake_word_enabled: e.target.checked });
});

document.getElementById("stt-threshold").addEventListener("input", (e) => {
    document.getElementById("stt-threshold-value").textContent = e.target.value;
});

document.getElementById("stt-threshold").addEventListener("change", async (e) => {
    await updateSTTConfig({ wake_word_threshold: parseFloat(e.target.value) });
});

document.getElementById("stt-listen-btn").addEventListener("click", () => {
    startListening();
});

document.getElementById("stt-stop-btn").addEventListener("click", () => {
    stopListening();
});

document.getElementById("stt-clear-btn").addEventListener("click", () => {
    clearTranscripts();
});

// Initial load
fetchSTTStatus().then((status) => {
    if (status && status.enabled) {
        startPolling();
    }
});
