const textInput = document.getElementById("textInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const result = document.getElementById("result");

const charCount = document.getElementById("charCount");
const wordCount = document.getElementById("wordCount");
const sentenceCount = document.getElementById("sentenceCount");

/* -----------------------------
   Live Statistics
------------------------------ */

function updateStats() {

    const text = textInput.value;

    charCount.textContent = text.length;

    wordCount.textContent =
        text.trim() === ""
            ? 0
            : text.trim().split(/\s+/).length;

    sentenceCount.textContent =
        text.trim() === ""
            ? 0
            : text.split(/[.!?]+/)
                  .filter(sentence => sentence.trim().length > 0)
                  .length;
}

textInput.addEventListener("input", updateStats);

/* -----------------------------
   Reset Page
------------------------------ */

function resetPage() {

    textInput.value = "";

    updateStats();

    result.innerHTML = `

        <div class="placeholder">

            <h2>Ready to Analyze</h2>

            <p>

                Enter or paste text above and click
                <strong>Analyze Text</strong>
                to begin.

            </p>

        </div>

    `;
}

/* -----------------------------
   Copy Results
------------------------------ */

function copyResults() {

    const prediction =
        document.getElementById("predictionText").innerText;

    const confidence =
        document.getElementById("confidenceValue").innerText;

    const reasons =
        [...document.querySelectorAll(".reason")]

        .map(reason => reason.innerText)

        .join("\n");

    const output =

`Prediction:
${prediction}

Confidence:
${confidence}

Reasons:
${reasons}`;

    navigator.clipboard.writeText(output);

    

}

/* -----------------------------
   Analyse Text
------------------------------ */

async function analyzeText() {

    const text = textInput.value.trim();

    if (!text) {

        alert("Please enter some text.");

        return;

    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";


    result.innerHTML = `

        <div class="loading">

            <div class="spinner"></div>

            <h2>Analyzing Text</h2>

            <p>Please wait while the model processes your input.</p>

        </div>

    `;

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                text

            })

        });

        if (!response.ok)
            throw new Error();

        const data = await response.json();

        

        const confidence =
            Number(data.confidence);

        let barColour;
        let confidenceLabel;

        if (confidence >= 80) {

            barColour = "#22c55e";
            confidenceLabel = "High Confidence";

        }

        else if (confidence >= 60) {

            barColour = "#eab308";
            confidenceLabel = "Medium Confidence";

        }

        else {

            barColour = "#ef4444";
            confidenceLabel = "Low Confidence";

        }

        const words =
            text.trim().split(/\s+/).length;

        const sentences =
            text.split(/[.!?]+/)
                .filter(sentence => sentence.trim().length > 0)
                .length;

        const reasons =
            Array.isArray(data.reasons)
                ? data.reasons
                : [];

        result.innerHTML = `

            <div class="result-card">

                <h2>Analysis Complete</h2>

                <div
                    id="predictionText"
                    class="result-title">

                    ${data.prediction}

                </div>

                <div class="confidence-section">

                    <div class="confidence-header">

                        <span>Confidence</span>

                        <strong
                            id="confidenceValue">

                            ${confidence}%

                        </strong>

                    </div>

                    <div class="progress-bar">

                        <div
                            class="progress-fill"
                            id="progressFill"
                            style="background:${barColour};">

                        </div>

                    </div>

                    <div class="confidence-label">

                        ${confidenceLabel}

                    </div>

                </div>

                <div class="statistics">

                    <div class="stat-box">

                        <h3>${text.length}</h3>

                        <p>Characters</p>

                    </div>

                    <div class="stat-box">

                        <h3>${words}</h3>

                        <p>Words</p>

                    </div>

                    <div class="stat-box">

                        <h3>${sentences}</h3>

                        <p>Sentences</p>

                    </div>

                    

                </div>

                <h3>Reasons for Prediction</h3>

                ${reasons.map(reason =>

                    `<div class="reason">

                        ${reason}

                    </div>`

                ).join("")}

                <div class="action-buttons">

                    <button
                        class="copy-btn"
                        onclick="copyResults()">

                        Copy Results

                    </button>

                </div>

            </div>

        `;

        setTimeout(() => {

            document.getElementById("progressFill").style.width =
                confidence + "%";

        }, 100);

    }

    catch {

        result.innerHTML = `

            <div class="result-card">

                <h2>Error</h2>

                <p>

                    Could not connect to the backend.

                </p>

            </div>

        `;

    }

    analyzeBtn.disabled = false;

    analyzeBtn.textContent = "Analyze Text";

}