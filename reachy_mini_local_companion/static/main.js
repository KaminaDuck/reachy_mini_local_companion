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

// === LLM Chat Controls ===
let profiles = [];
let currentProfileId = null;
let chatMessages = [];
let isSending = false;

async function loadProfiles() {
    try {
        const resp = await fetch("/profiles");
        profiles = await resp.json();
        populateProfileSelect();
        return profiles;
    } catch (e) {
        console.error("Error loading profiles:", e);
        return [];
    }
}

function populateProfileSelect() {
    const select = document.getElementById("profile-select");
    select.innerHTML = profiles
        .map(
            (p) =>
                `<option value="${p.id}" ${p.id === currentProfileId ? "selected" : ""}>${p.name}</option>`
        )
        .join("");

    // Set initial profile if not set
    if (!currentProfileId && profiles.length > 0) {
        currentProfileId = profiles[0].id;
    }
}

async function selectProfile(profileId) {
    currentProfileId = profileId;
    // Clear history when switching profiles
    await clearChatHistory();
}

async function fetchChatStatus() {
    try {
        const resp = await fetch("/chat/status");
        const status = await resp.json();
        updateChatStatusUI(status);
        return status;
    } catch (e) {
        console.error("Error fetching chat status:", e);
        return null;
    }
}

function updateChatStatusUI(status) {
    const statusEl = document.getElementById("llm-status");
    const textEl = statusEl.querySelector(".status-text");

    if (status.connected) {
        statusEl.className = "llm-status connected";
        textEl.textContent = `${status.provider}:${status.model}`;
    } else if (status.error) {
        statusEl.className = "llm-status error";
        textEl.textContent = "Error";
    } else {
        statusEl.className = "llm-status disconnected";
        textEl.textContent = "Not connected";
    }

    // Update current profile if provided
    if (status.current_profile_id) {
        currentProfileId = status.current_profile_id;
        const select = document.getElementById("profile-select");
        select.value = currentProfileId;
    }
}

async function sendMessage() {
    const input = document.getElementById("chat-input");
    const message = input.value.trim();

    if (!message || isSending) return;

    isSending = true;
    const sendBtn = document.getElementById("chat-send-btn");
    sendBtn.disabled = true;
    sendBtn.textContent = "Sending...";

    // Add user message to UI
    addMessageToUI("user", message);
    input.value = "";

    try {
        const resp = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: message,
                profile_id: currentProfileId,
            }),
        });
        const data = await resp.json();

        if (data.error) {
            addMessageToUI("error", data.error);
        } else {
            addMessageToUI("assistant", data.message);
        }

        // Refresh status to update connection state
        await fetchChatStatus();
    } catch (e) {
        console.error("Error sending message:", e);
        addMessageToUI("error", "Failed to send message. Check your LLM configuration.");
    } finally {
        isSending = false;
        sendBtn.disabled = false;
        sendBtn.textContent = "Send";
    }
}

function addMessageToUI(role, content) {
    const container = document.getElementById("chat-messages");

    // Remove placeholder if present
    const placeholder = container.querySelector(".placeholder");
    if (placeholder) {
        placeholder.remove();
    }

    const messageEl = document.createElement("div");
    messageEl.className = `chat-message ${role}`;

    const roleLabel = role === "user" ? "You" : role === "assistant" ? "Reachy" : "Error";
    messageEl.innerHTML = `
        <span class="message-role">${roleLabel}</span>
        <span class="message-content">${escapeHtml(content)}</span>
    `;

    container.appendChild(messageEl);
    container.scrollTop = container.scrollHeight;

    // Track messages
    if (role !== "error") {
        chatMessages.push({ role, content });
    }
}

async function clearChatHistory() {
    try {
        await fetch("/chat/history", { method: "DELETE" });
        chatMessages = [];
        const container = document.getElementById("chat-messages");
        container.innerHTML = '<p class="placeholder">Send a message to start chatting with Reachy.</p>';
    } catch (e) {
        console.error("Error clearing chat history:", e);
    }
}

async function loadChatHistory() {
    try {
        const resp = await fetch("/chat/history");
        const history = await resp.json();

        if (history.length > 0) {
            const container = document.getElementById("chat-messages");
            container.innerHTML = "";

            for (const msg of history) {
                addMessageToUI(msg.role, msg.content);
            }
        }
    } catch (e) {
        console.error("Error loading chat history:", e);
    }
}

// === Profile Management Modal ===
function openProfileModal() {
    const modal = document.getElementById("profile-modal");
    modal.classList.remove("hidden");
    renderProfileList();
    resetProfileForm();
}

function closeProfileModal() {
    const modal = document.getElementById("profile-modal");
    modal.classList.add("hidden");
}

function renderProfileList() {
    const listEl = document.getElementById("profile-list");
    listEl.innerHTML = profiles
        .map(
            (p) => `
        <div class="profile-item">
            <div class="profile-info">
                <strong>${escapeHtml(p.name)}</strong>
                <span>${escapeHtml(p.description || "")}</span>
            </div>
            <div class="profile-actions">
                <button onclick="editProfile('${p.id}')" class="edit-btn">Edit</button>
                <button onclick="deleteProfile('${p.id}')" class="delete-btn">Delete</button>
            </div>
        </div>
    `
        )
        .join("");
}

function resetProfileForm() {
    document.getElementById("profile-form-title").textContent = "Create New Profile";
    document.getElementById("edit-profile-id").value = "";
    document.getElementById("profile-name").value = "";
    document.getElementById("profile-description").value = "";
    document.getElementById("profile-prompt").value = "";
}

function editProfile(profileId) {
    const profile = profiles.find((p) => p.id === profileId);
    if (!profile) return;

    document.getElementById("profile-form-title").textContent = "Edit Profile";
    document.getElementById("edit-profile-id").value = profile.id;
    document.getElementById("profile-name").value = profile.name;
    document.getElementById("profile-description").value = profile.description || "";
    document.getElementById("profile-prompt").value = profile.system_prompt;
}

async function saveProfile() {
    const editId = document.getElementById("edit-profile-id").value;
    const name = document.getElementById("profile-name").value.trim();
    const description = document.getElementById("profile-description").value.trim();
    const systemPrompt = document.getElementById("profile-prompt").value.trim();

    if (!name || !systemPrompt) {
        alert("Name and system prompt are required.");
        return;
    }

    try {
        let resp;
        if (editId) {
            // Update existing profile
            resp = await fetch(`/profiles/${editId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: name,
                    description: description,
                    system_prompt: systemPrompt,
                }),
            });
        } else {
            // Create new profile
            resp = await fetch("/profiles", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: name,
                    description: description,
                    system_prompt: systemPrompt,
                }),
            });
        }

        const data = await resp.json();
        if (data.error) {
            alert(data.error);
        } else {
            await loadProfiles();
            renderProfileList();
            resetProfileForm();
        }
    } catch (e) {
        console.error("Error saving profile:", e);
        alert("Failed to save profile.");
    }
}

async function deleteProfile(profileId) {
    if (!confirm("Are you sure you want to delete this profile?")) {
        return;
    }

    try {
        const resp = await fetch(`/profiles/${profileId}`, { method: "DELETE" });
        const data = await resp.json();

        if (data.error) {
            alert(data.error);
        } else {
            await loadProfiles();
            renderProfileList();
        }
    } catch (e) {
        console.error("Error deleting profile:", e);
        alert("Failed to delete profile.");
    }
}

// Chat Event Listeners
document.getElementById("profile-select").addEventListener("change", (e) => {
    selectProfile(e.target.value);
});

document.getElementById("chat-send-btn").addEventListener("click", () => {
    sendMessage();
});

document.getElementById("chat-input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});

document.getElementById("chat-clear-btn").addEventListener("click", () => {
    clearChatHistory();
});

// Profile Modal Event Listeners
document.getElementById("manage-profiles-btn").addEventListener("click", () => {
    openProfileModal();
});

document.getElementById("modal-close-btn").addEventListener("click", () => {
    closeProfileModal();
});

document.getElementById("profile-save-btn").addEventListener("click", () => {
    saveProfile();
});

document.getElementById("profile-cancel-btn").addEventListener("click", () => {
    resetProfileForm();
});

// Close modal when clicking outside
document.getElementById("profile-modal").addEventListener("click", (e) => {
    if (e.target.id === "profile-modal") {
        closeProfileModal();
    }
});

// Initialize LLM Chat
loadProfiles().then(() => {
    fetchChatStatus();
    loadChatHistory();
});
