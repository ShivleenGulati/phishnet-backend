document.addEventListener('DOMContentLoaded', function() {
    
    const scanBtn = document.getElementById("scanBtn");
    const shieldWrap = document.getElementById("shield-wrap");
    const shieldIcon = document.getElementById("shield-icon");
    const statusText = document.getElementById("status-text");
    const detailsBox = document.getElementById("details-box");
    
    // Values
    const verdictVal = document.getElementById("verdict-val");
    const confVal = document.getElementById("conf-val");
    const sourceVal = document.getElementById("source-val");

    scanBtn.addEventListener("click", function() {
        // 1. START ANIMATION (Scanning Mode)
        shieldWrap.className = "shield-wrapper scanning"; // Adds pulse effect
        shieldIcon.innerText = "📡";
        statusText.innerText = "Analyzing Threat Vectors...";
        statusText.style.color = "#2563eb";
        detailsBox.style.display = "none";
        scanBtn.disabled = true;
        scanBtn.innerHTML = "Scanning...";

        // 2. GET URL
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            let currentUrl = tabs[0].url;

            // 3. CALL API
            fetch('http://127.0.0.1:5000/check-url', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: currentUrl })
            })
            .then(response => response.json())
            .then(data => {
                // 4. UPDATE UI (Stop Animation)
                shieldWrap.classList.remove("scanning");
                detailsBox.style.display = "grid"; // Show grid
                scanBtn.disabled = false;
                scanBtn.innerHTML = "Scan Again";

                if (data.result === "PHISHING") {
                    // DANGER STATE
                    shieldWrap.className = "shield-wrapper status-danger";
                    shieldIcon.innerText = "💀";
                    statusText.innerText = "MALICIOUS SITE DETECTED";
                    statusText.style.color = "#ef4444";
                    verdictVal.style.color = "#ef4444";
                } else {
                    // SAFE STATE
                    shieldWrap.className = "shield-wrapper status-safe";
                    shieldIcon.innerText = "🛡️";
                    statusText.innerText = "SITE IS SECURE";
                    statusText.style.color = "#10b981";
                    verdictVal.style.color = "#10b981";
                }

                // Fill Data
                verdictVal.innerText = data.result;
                confVal.innerText = data.confidence + "%";
                sourceVal.innerText = data.source;
            })
            .catch(error => {
                console.error('Error:', error);
                shieldWrap.classList.remove("scanning");
                shieldIcon.innerText = "❌";
                statusText.innerText = "Connection Failed";
                statusText.style.color = "black";
                scanBtn.disabled = false;
                scanBtn.innerHTML = "Retry Connection";
            });
        });
    });
});