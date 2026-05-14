const BASE_URL = "http://127.0.0.1:5000";

document.getElementById("signupForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const name      = document.getElementById("fullname").value.trim();
    const email     = document.getElementById("email").value.trim();
    const carnumber = document.getElementById("carnumber").value.trim().toUpperCase();
    const password  = document.getElementById("password").value;
    const confirm   = document.getElementById("confirmpassword").value;
    const errormsg  = document.getElementById("errormsg");


    if (!name || !email || !carnumber || !password || !confirm) {
        errormsg.textContent = "All fields are required!";
        return;
    }

    if (password !== confirm) {
        errormsg.textContent = "Passwords do not match!";
        return;
    }

    if (password.length < 6) {
        errormsg.textContent = "Password must be at least 6 characters!";
        return;
    }


    try {
        const response = await fetch(`${BASE_URL}/auth/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, carnumber, password })
        });

        const result = await response.json();

        if (response.ok) {
            alert("Account created successfully!");
            window.location.href = "login.html";
        } else {
            errormsg.textContent = result.error || "Signup failed!";
        }

    } catch (error) {
        errormsg.textContent = "Cannot connect to server. Try again!";
    }
});
