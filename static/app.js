const API_BASE_URL = "";

const form = document.getElementById("tripForm");
const message = document.getElementById("message");
const origin = document.getElementById("origin");
const destination = document.getElementById("destination");
const duration = document.getElementById("duration");
const travelers = document.getElementById("travelers");
const style = document.getElementById("style");
const budget = document.getElementById("budget");
const errorBox = document.getElementById("errorBox");
const samplePromptButton = document.getElementById("samplePrompt");
const surpriseButton = document.getElementById("surpriseButton");
const sendButton = document.getElementById("sendButton");
const chatStream = document.getElementById("chatStream");
const chatInput = document.getElementById("chatInput");
const itineraryOutput = document.getElementById("itineraryOutput");
const dayList = document.getElementById("dayList");

function showError(text) {
  if (errorBox) {
    errorBox.textContent = text;
    errorBox.classList.add("visible");
  }
}

function clearError() {
  if (errorBox) {
    errorBox.textContent = "";
    errorBox.classList.remove("visible");
  }
}

function addChatMessage(text, type = "bot") {
  if (!chatStream) return;

  const row = document.createElement("div");
  row.className = `${type === "bot" ? "chat-row bot-row" : "chat-row user-row"}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = type === "bot" ? "AI" : "You";

  const bubble = document.createElement("div");
  bubble.className = "chat-bubble";

  const title = document.createElement("div");
  title.className = "chat-bubble-title";
  title.textContent = type === "bot" ? "TripMate AI" : "You";

  const messageText = document.createElement(type === "bot" ? "div" : "p");
  if (type === "bot") {
    messageText.innerHTML = formatItinerary(text);
  } else {
    messageText.textContent = text;
  }

  bubble.appendChild(title);
  bubble.appendChild(messageText);

  row.appendChild(avatar);
  row.appendChild(bubble);

  chatStream.appendChild(row);
  chatStream.scrollTop = chatStream.scrollHeight;
}

function addTyping() {
  if (!chatStream) return;

  const loader = document.createElement("div");
  loader.className = "chat-row bot-row";
  loader.id = "loader-row";

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = "AI";

  const bubble = document.createElement("div");
  bubble.className = "chat-bubble";

  const inner = document.createElement("div");
  inner.className = "loader";
  inner.innerHTML = `<span class="loader-dot"></span><span class="loader-text">Thinking...</span>`;

  bubble.appendChild(inner);
  loader.appendChild(avatar);
  loader.appendChild(bubble);

  chatStream.appendChild(loader);
  chatStream.scrollTop = chatStream.scrollHeight;
}

function removeTyping() {
  const loaderRow = document.getElementById("loader-row");
  if (loaderRow) loaderRow.remove();
}

function fallbackItinerary(text) {
  const route = `${origin?.value || "Origin"} → ${destination?.value || "Destination"}`;
  const fallback = `## Plan overview
- Route: ${route}
- Duration: ${duration?.value || "your selected duration"}
- Travelers: ${travelers?.value || "your group"}

## Day 1
- Morning: Arrive and settle into your hotel in ${destination?.value || "the destination"}.
- Afternoon: Explore a short city walk and local food stops.
- Evening: Relax and enjoy a local dinner.

## Day 2
- Morning: Visit a cultural or heritage location.
- Afternoon: Continue with a local market or scenic route.
- Evening: Free time and a recommended dinner.

## Day 3
- Morning: Explore a nature or attraction experience.
- Afternoon: Take a short rest or optional activity break.
- Evening: Enjoy the destination night atmosphere.

## Extra suggestions
- Keep travel flexible for weather and local timing.
- Book hotels near major tourist areas.
- Ask local guides for food and cultural experiences.`;

  return fallback;
}

function formatItinerary(answer) {
  const lines = String(answer).replace(/\r\n/g, "\n").split("\n");
  const blocks = [];

  lines.forEach((line) => {
    const trimmed = line.trim();
    if (!trimmed) return;
    if (trimmed.startsWith("##")) {
      blocks.push(`<div class="itinerary-heading">${trimmed.replace(/^##\s*/, "")}</div>`);
    } else if (trimmed.startsWith("- ")) {
      blocks.push(`<div class="itinerary-bullet">${trimmed.replace(/^-\s*/, "")}</div>`);
    } else {
      blocks.push(`<div class="itinerary-paragraph">${trimmed}</div>`);
    }
  });

  return `<div class="formatted-output">${blocks.join("")}</div>`;
}

function parseDayItems(answer) {
  const lines = String(answer).split("\n");
  const days = [];

  lines.forEach((line) => {
    const match = line.match(/^\s*##\s*Day\s*(\d+)/i);
    if (match) {
      const label = line.replace(/^\s*##\s*Day\s*\d+\s*[:\-]?\s*/i, "");
      days.push({ day: Number(match[1]), title: label || "Travel route" });
    }
  });

  return days;
}

function renderPlannerOutput(answer) {
  if (!itineraryOutput) return;

  itineraryOutput.innerHTML = formatItinerary(answer);

  if (dayList) {
    const days = parseDayItems(answer);
    if (days.length > 0) {
      dayList.innerHTML = "";
      days.forEach((item) => {
        const row = document.createElement("article");
        row.className = "day-item";
        row.innerHTML = `
          <span class="day-marker">Day ${item.day}</span>
          <div class="day-card-body">
            <span class="day-route">Itinerary</span>
            <span class="day-place">${item.title || "Travel route"}</span>
          </div>
        `;
        dayList.appendChild(row);
      });
    }
  }
}

function generateThreadId() {
  return "thread_" + Math.random().toString(36).slice(2, 10);
}

async function sendTripRequest(text) {
  const payload = {
    message: text,
    thread_id: generateThreadId()
  };

  try {
    const response = await fetch(`${API_BASE_URL}/api/travel`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error("Planner failed");
    }

    const data = await response.json();
    const answer = data.answer || data.itinerary || "";

    if (chatStream) {
      removeTyping();
      addChatMessage(answer || fallbackItinerary(text), "bot");
    }

    if (itineraryOutput) {
      renderPlannerOutput(answer || fallbackItinerary(text));
    }

    return answer;
  } catch (error) {
    if (chatStream) {
      removeTyping();
      addChatMessage(fallbackItinerary(text), "bot");
    }

    if (itineraryOutput) {
      renderPlannerOutput(fallbackItinerary(text));
    }

    return fallbackItinerary(text);
  }
}

if (form && message) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearError();

    const text = message.value.trim();
    if (!text) {
      showError("Please describe your trip idea before generating an itinerary.");
      return;
    }

    addChatMessage(text, "user");
    addTyping();

    sendTripRequest(text);
  });
}

if (chatStream && chatInput && sendButton) {
  sendButton.addEventListener("click", async () => {
    const text = chatInput.value.trim();
    if (!text) return;

    addChatMessage(text, "user");
    addTyping();
    chatInput.value = "";

    sendTripRequest(text);
  });
}

if (samplePromptButton) {
  samplePromptButton.addEventListener("click", () => {
    const samples = [
      "Plan a 5-day holiday from New Delhi to Goa for two travelers.",
      "Create a relaxing 6-day beach vacation from Delhi to Kerala.",
      "Plan a 7-day food and culture trip from Mumbai to Jaipur."
    ];

    const random = samples[Math.floor(Math.random() * samples.length)];
    message.value = random;

    if (random.includes("Goa")) {
      origin.value = "New Delhi";
      destination.value = "Goa";
      duration.value = "5 days";
      travelers.value = "2 travelers";
      style.value = "Nature & Heritage";
    } else if (random.includes("Kerala")) {
      origin.value = "Delhi";
      destination.value = "Kerala";
      duration.value = "6 days";
      style.value = "Relaxation";
    } else {
      origin.value = "Mumbai";
      destination.value = "Jaipur";
      duration.value = "7 days";
      style.value = "Food & Culture";
    }
  });
}

if (surpriseButton) {
  surpriseButton.addEventListener("click", () => {
    const destinations = ["Goa", "Jaipur", "Darjeeling", "Kerala", "Leh"];
    const randomDestination = destinations[Math.floor(Math.random() * destinations.length)];
    destination.value = randomDestination;
    origin.value = "New Delhi";
    duration.value = "5 days";
    travelers.value = "2 travelers";
    message.value = `Plan a ${duration.value} trip from ${origin.value} to ${destination.value} for ${travelers.value}.`;
  });
}

if (sendButton && form) {
  sendButton.addEventListener("click", () => {
    if (form) form.requestSubmit();
  });
}

document.getElementById("themeToggle")?.addEventListener("click", () => {
  document.body.classList.toggle("dark");
});
