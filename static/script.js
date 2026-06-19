const textInput =
    document.getElementById("textInput");

const counter =
    document.getElementById("counter");

textInput.addEventListener("input", () => {

    counter.textContent =
        textInput.value.length + " characters";

});

async function analyzeText() {

    const text =
        textInput.value.trim();

    if (text === "") {

        alert("Please enter some text.");

        return;
    }

    document.getElementById("result").innerHTML = `
        <p class="loading">
            Analyzing...
        </p>
    `;

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        });

        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );

        }

        const data =
            await response.json();

        const predictionClass =
            data.prediction.includes("AI")
                ? "ai"
                : "human";

        document.getElementById("result").innerHTML = `

            <div class="result-card">

                <h2 class="${predictionClass}">
                    ${data.prediction}
                </h2>

                <p>
                    <strong>Confidence:</strong>
                    ${data.confidence}%
                </p>

                <h3>Reasons</h3>

                <ul>
                    ${data.reasons
                        .map(reason =>
                            `<li>${reason}</li>`)
                        .join("")}
                </ul>

            </div>

        `;

    }

    catch (error) {

        console.error(error);

        document.getElementById("result").innerHTML = `

            <div class="result-card">

                <h2>Error</h2>

                <p>
                    Could not connect to backend.
                </p>

                <p>
                    Make sure Flask is running.
                </p>

            </div>

        `;
    }
}