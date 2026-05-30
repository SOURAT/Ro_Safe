const token = localStorage.getItem("token");
const role  = localStorage.getItem("role");

if (!token || role !== "user") {
    alert("Please login first!");
    window.location.href = "/index.html";
}


function toggleMenu() {
    const navLinks = document.getElementById("nav-links");
    navLinks.classList.toggle("active");
}


document.getElementById("logoutBtn").addEventListener("click", function(e) {
    e.preventDefault();
    localStorage.clear();
    window.location.href = "/index.html";
});


window.addEventListener("load", async function() {
    const errormsg = document.getElementById("errormsg");
    const loading  = document.getElementById("loadingMsg");

    try {
        const response = await fetch(`${BASE_URL}/history/my-history`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const result = await response.json();
        loading.style.display = "none";

        if (response.ok) {
            displayFines(result.records);
        } else {
            errormsg.textContent = result.error || "Failed to load fines!";
        }

    } catch (error) {
        loading.style.display = "none";
        errormsg.textContent = "Cannot connect to server. Try again!";
    }
});


function displayFines(records) {
    const finesDisplay = document.getElementById("finesDisplay");
    finesDisplay.innerHTML = "";

    if (!records || records.length === 0) {
        finesDisplay.innerHTML = `
            <div class="no-fines">
                <p>🎉 You have no fines yet!</p>
            </div>`;
        return;
    }

    records.forEach((record, index) => {
        
        window._fineRecords = window._fineRecords || [];
        window._fineRecords[index] = record;

        const card = document.createElement("div");
        card.className = "fine-card";

        const statusClass = record.status === "paid"
            ? "status-paid"
            : "status-unpaid";

        card.innerHTML = `
            <h3>${record.violation}</h3>
            <p><b>Vehicle Number:</b> ${record.vehicle_number}</p>
            <p><b>Vehicle Type:</b> ${record.vehicle_type}</p>
            <p><b>Fine:</b> ₹${record.fine}</p>
            <p><b>Repeated:</b> ${record.repeated ? "Yes" : "No"}</p>
            <p><b>Date:</b> ${new Date(record.date).toLocaleDateString()}</p>
            <p><b>Status:</b>
                <span class="${statusClass}">
                    ${record.status ? record.status.toUpperCase() : "UNPAID"}
                </span>
            </p>
            <button class="download-btn" data-index="${index}">
                Download Receipt
            </button>
        `;
        finesDisplay.appendChild(card);
    });

   
    document.getElementById("finesDisplay").addEventListener("click", function(e) {
        if (e.target.classList.contains("download-btn")) {
            const index  = e.target.getAttribute("data-index");
            const record = window._fineRecords[index];
            downloadReceipt(record);
        }
    });
}


async function downloadReceipt(record) {
    try {
        const response = await fetch(`${BASE_URL}/fine/generate-receipt`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(record)
        });

        if (response.ok) {
            const blob = await response.blob();
            const url  = window.URL.createObjectURL(blob);
            const a    = document.createElement("a");
            a.href     = url;
            a.download = `receipt_${record.vehicle_number}.pdf`;
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            alert("Failed to generate receipt!");
        }

    } catch (error) {
        alert("Cannot connect to server. Try again!");
    }
}
