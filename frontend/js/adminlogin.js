const BASE_URL = "https://road-safety-legal.onrender.com";

document.getElementById("adminLoginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const key      = document.getElementById("key").value.trim();
    const password = document.getElementById("password").value;
    const errormsg = document.getElementById("errormsg");


    if (!key || !password) {
        errormsg.textContent = "All fields are required!";
        return;
    }


    try {
        const response = await fetch(`${BASE_URL}/auth/admin-login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key, password })
        });

        const result = await response.json();

        if (response.ok) {

            localStorage.setItem("token", result.token);
            localStorage.setItem("role", "admin");
            localStorage.setItem("adminKey", key);
            window.location.href = "admin.html";
        } else {
            errormsg.textContent = result.error || "Login failed!";
        }

    } catch (error) {
        errormsg.textContent = "Cannot connect to server. Try again!";
    }
});
