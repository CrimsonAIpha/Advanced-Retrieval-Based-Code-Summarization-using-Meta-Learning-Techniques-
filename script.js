function summarizeCode() {
    const codeInput = document.getElementById("codeInput").value;
    if (!codeInput.trim()) {
        document.getElementById("output").innerText = "Error: Please enter some Python code.";
        return;
    }

    fetch("http://127.0.0.1:5000/summarize", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: codeInput })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById("output").innerText = data.summary || "Error: Failed to generate a summary.";
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("output").innerText = "Error: Failed to summarize the code. Please try again.";
        });
}

document.addEventListener("DOMContentLoaded", () => {
    document.body.style.backgroundColor = "#1e1e1e";
    document.body.style.color = "#ffffff";
});
