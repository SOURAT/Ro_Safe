const token = localStorage.getItem("token");
const role  = localStorage.getItem("role");

if (!token) {
    alert("Please login first!");
    window.location.href = "/index.html";
}


const data = JSON.parse(localStorage.getItem("receiptData"));

if (!data) {
    document.getElementById("errormsg").textContent = "No receipt data found!";
    document.getElementById("downloadBtn").style.display = "none";
} else {

    document.getElementById("vehicleNumber").textContent = data.vehicle_number;
    document.getElementById("vehicleType").textContent   = data.vehicle_type;
    document.getElementById("violation").textContent     = data.violation;
    document.getElementById("fine").textContent          = data.fine;
    document.getElementById("repeated").textContent      = data.repeated ? "Yes" : "No";
}


document.getElementById("downloadBtn").addEventListener("click", async function() {
    const errormsg = document.getElementById("errormsg");

    if (!data) {
        errormsg.textContent = "No receipt data found!";
        return;
    }

    try {
        const response = await generateReceipt(data);

        if (response && response.ok) {
            const blob = await response.blob();
            const url  = window.URL.createObjectURL(blob);
            const a    = document.createElement("a");
            a.href     = url;
            a.download = "receipt.pdf";
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            errormsg.textContent = "Failed to generate receipt!";
        }

    } catch (error) {
        errormsg.textContent = "Cannot connect to server. Try again!";
    }
});
