
const token = localStorage.getItem("token");
const role  = localStorage.getItem("role");

if (!token || role !== "user") {
    alert("Please login first!");
    window.location.href = "index.html";
}


function toggleMenu() {
    const navLinks = document.getElementById("nav-links");
    navLinks.classList.toggle("active");
}

document.getElementById("logoutBtn").addEventListener("click", function(e) {
    e.preventDefault();
    localStorage.clear();
    window.location.href = "index.html";
});

window.addEventListener("load", async function() {
    const state    = localStorage.getItem("state");
    const district = localStorage.getItem("district");
    const city     = localStorage.getItem("city");
    const errormsg = document.getElementById("errormsg");
    const loading  = document.getElementById("loadingMsg");


    if (state) {
        document.getElementById("locationInfo").textContent
            = `📍 Showing rules for: ${city}, ${state}`;
    } else {
        document.getElementById("locationInfo").textContent
            = "📍 Location not detected";
        loading.style.display = "none";
        errormsg.textContent
            = "Please go back to main page to detect your location first!";
        return;
    }


    try {
        const response = await fetch(
            `${BASE_URL}/rules/?state=${state}&district=${district}&city=${city}`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const result = await response.json();
        loading.style.display = "none";

        if (response.ok) {
            displayRules(result.rules);
        } else {
            errormsg.textContent = result.error || "Failed to load rules!";
        }

    } catch (error) {
        loading.style.display = "none";
        errormsg.textContent = "Cannot connect to server. Try again!";
    }
});


function displayRules(rules) {
    const rulesDisplay = document.getElementById("rulesDisplay");
    rulesDisplay.innerHTML = "";

    const keys = Object.keys(rules);

    if (keys.length === 0) {
        rulesDisplay.innerHTML = `
            <div class="no-rules">
                <p>No rules found for your location yet!</p>
            </div>`;
        return;
    }

    keys.forEach(violation => {
        const rule = rules[violation];

        let fineText = "";
        if (typeof rule.fine === "object") {
            fineText = `₹${rule.fine.min} - ₹${rule.fine.max}`;
        } else {
            fineText = `₹${rule.fine}`;
        }

        const card = document.createElement("div");
        card.className = "rule-card";
        card.innerHTML = `
            <h3>${violation.replace(/_/g, " ")}</h3>
            <p><b>Description:</b> ${rule.description || "-"}</p>
            <br>
            <span class="fine-badge">₹ ${fineText}</span>
            <span class="section-badge">${rule.section || "-"}</span>
        `;
        rulesDisplay.appendChild(card);
    });
}
