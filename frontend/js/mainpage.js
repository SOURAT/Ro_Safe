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

window.addEventListener("load", function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            async function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                try {
                    const response = await fetch(`${BASE_URL}/location/`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Authorization": `Bearer ${token}`
                        },
                        body: JSON.stringify({ latitude: lat, longitude: lon })
                    });

                    const result = await response.json();

                    if (response.ok) {
                        localStorage.setItem("state",    result.state    || "");
                        localStorage.setItem("city",     result.city     || "");
                        localStorage.setItem("district", result.district || "");
                        localStorage.setItem("country",  result.country  || "");

                        document.getElementById("locationInfo").textContent
                            = `📍 ${result.city}, ${result.state}, ${result.country}`;
                    }

                } catch (error) {
                    console.log("Location fetch failed:", error);
                }
            },
            function(error) {
                console.log("Geolocation denied:", error);
            }
        );
    }
});
