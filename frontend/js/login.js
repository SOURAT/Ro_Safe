const BASE_URL = "https://road-safety-legal.onrender.com/";

document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const email    = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const errormsg = document.getElementById("errormsg");


    if (!email || !password) {
        errormsg.textContent = "All fields are required!";
        return;
    }


    try {
        const response = await fetch(`${BASE_URL}/auth/user-login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();

        if (response.ok) {

            localStorage.setItem("token", result.token);
            localStorage.setItem("role", "user");
            localStorage.setItem("email", email);
            window.location.href = "mainpage.html";
        } else {
            errormsg.textContent = result.error || "Login failed!";
        }

    } catch (error) {
        errormsg.textContent = "Cannot connect to server. Try again!";
    }
});
