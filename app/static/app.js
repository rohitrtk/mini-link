const form = document.querySelector("#shorten-form");
const urlInput = document.querySelector("#url-input");
const submitButton = document.querySelector("#submit-button");
const errorMessage = document.querySelector("#form-error");
const resultPanel = document.querySelector("#result-panel");
const shortUrlLink = document.querySelector("#short-url");
const resultMeta = document.querySelector("#result-meta");
const copyButton = document.querySelector("#copy-button");

let currentShortUrl = "";

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  submitButton.setAttribute("aria-busy", String(isLoading));
  submitButton.querySelector("span:first-child").textContent = isLoading
    ? "Making it mini…"
    : "Create mini link";
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
  resultPanel.hidden = true;
}

function clearMessages() {
  errorMessage.hidden = true;
  errorMessage.textContent = "";
}

function showResult(data) {
  currentShortUrl = new URL(`/${data.short_code}`, window.location.origin).href;

  shortUrlLink.href = currentShortUrl;
  shortUrlLink.textContent = currentShortUrl;

  const creationCount = Number(data.number_of_creations ?? 1);
  resultMeta.textContent = creationCount === 1
    ? "Freshly created."
    : `Created ${creationCount.toLocaleString()} times.`;

  copyButton.textContent = "Copy";
  resultPanel.hidden = false;
}

async function copyShortUrl() {
  if (!currentShortUrl) return;

  try {
    await navigator.clipboard.writeText(currentShortUrl);
    copyButton.textContent = "Copied!";
  } catch {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(shortUrlLink);
    selection.removeAllRanges();
    selection.addRange(range);
    copyButton.textContent = "Select & copy";
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessages();

  if (!form.checkValidity()) {
    form.reportValidity();
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/shorten", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: urlInput.value.trim() }),
    });

    const data = await response.json();

    if (!response.ok) {
      const detail = Array.isArray(data.detail)
        ? data.detail.map((item) => item.msg).join(" ")
        : data.detail;
      throw new Error(detail || "Mini Link could not shorten that URL.");
    }

    showResult(data);
  } catch (error) {
    showError(error.message || "Something went wrong. Please try again.");
  } finally {
    setLoading(false);
  }
});

copyButton.addEventListener("click", copyShortUrl);
