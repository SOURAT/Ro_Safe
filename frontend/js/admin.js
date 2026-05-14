const BASE_URL = "http://127.0.0.1:5000";

const token = localStorage.getItem("token");
const role  = localStorage.getItem("role");

if (!token || role !== "admin") {
    alert("Access denied! Admins only.");
    window.location.href = "adminlogin.html";
}



document.getElementById("logoutBtn").addEventListener("click", function(e) {
    e.preventDefault();
    localStorage.clear();
    window.location.href = "index.html";
});



document.getElementById("fineForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const vehicle_type   = document.getElementById("vehicle_type").value;
    const violation      = document.getElementById("violation").value;
    const state          = document.getElementById("state").value;
    const vehicle_number = document.getElementById("vehicle_number").value.trim().toUpperCase();
    const fineError      = document.getElementById("fineError");
    const fineResult     = document.getElementById("fineResult");

    fineError.textContent = "";
    fineResult.style.display = "none";

    if (!vehicle_type || !violation || !state || !vehicle_number) {
        fineError.textContent = "All fields are required!";
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/fine/calculate-fine`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ vehicle_type, violation, state, vehicle_number })
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem("receiptData", JSON.stringify(result));
            document.getElementById("resultVehicle").textContent   = `Vehicle Number: ${result.vehicle_number}`;
            document.getElementById("resultViolation").textContent = `Violation: ${result.violation}`;
            document.getElementById("resultFine").textContent      = `Fine: ₹${result.fine}`;
            document.getElementById("resultRepeated").textContent  = `Repeated: ${result.repeated ? "Yes" : "No"}`;
            fineResult.style.display = "block";
            window.lastFineResult = result;

        } else {
            fineError.textContent = result.error || "Failed to calculate fine!";
        }

    } catch (error) {
        fineError.textContent = "Cannot connect to server. Try again!";
    }
});



document.getElementById("downloadBtn").addEventListener("click", async function() {
    const result = window.lastFineResult;

    if (!result) return;

    try {
        const response = await fetch(`${BASE_URL}/fine/generate-receipt`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(result)
        });

        if (response.ok) {
            const blob = await response.blob();
            const url  = window.URL.createObjectURL(blob);
            const a    = document.createElement("a");
            a.href     = url;
            a.download = "receipt.pdf";
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            alert("Failed to generate receipt!");
        }

    } catch (error) {
        alert("Cannot connect to server. Try again!");
    }
});



document.getElementById("searchBtn").addEventListener("click", async function() {
    const vehicle        = document.getElementById("hist").value.trim().toUpperCase();
    const histError      = document.getElementById("histError");
    const historyDisplay = document.getElementById("historyDisplay");

    histError.textContent    = "";
    historyDisplay.innerHTML = "";

    if (!vehicle) {
        histError.textContent = "Please enter a vehicle number!";
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/history/fine-history?vehicle=${vehicle}`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        const result = await response.json();

        if (response.ok) {
            if (result.count === 0) {
                historyDisplay.innerHTML = "<p>No history found for this vehicle.</p>";
                return;
            }

            result.records.forEach(record => {
                const div = document.createElement("div");
                div.style.borderBottom = "1px solid #ccc";
                div.style.padding = "8px 0";
                div.innerHTML = `
                    <p><b>Violation:</b> ${record.violation}</p>
                    <p><b>Fine:</b> ₹${record.fine}</p>
                    <p><b>Vehicle Type:</b> ${record.vehicle_type}</p>
                    <p><b>Repeated:</b> ${record.repeated ? "Yes" : "No"}</p>
                    <p><b>Date:</b> ${new Date(record.date).toLocaleDateString()}</p>
                    <button onclick="downloadHistoryReceipt(${JSON.stringify(record)})">
                        Download Receipt
                    </button>
                `;
                historyDisplay.appendChild(div);
            });

        } else {
            histError.textContent = result.error || "Failed to fetch history!";
        }

    } catch (error) {
        histError.textContent = "Cannot connect to server. Try again!";
    }
});



async function downloadHistoryReceipt(record) {
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
