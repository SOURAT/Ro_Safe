const BASE_URL = "https://road-safety-legal.onrender.com";



function getToken() {
    return localStorage.getItem("token");
}


async function fetchRules() {
    const state    = localStorage.getItem("state");
    const district = localStorage.getItem("district");
    const city     = localStorage.getItem("city");
    const road     = localStorage.getItem("road");

    if (!state) {
        return { error: "Location not detected yet" };
    }

    try {
        const response = await fetch(
            `${BASE_URL}/rules/?state=${state}&district=${district}&city=${city}&road=${road}`,
            {
                headers: {
                    "Authorization": `Bearer ${getToken()}`
                }
            }
        );
        return response.json();

    } catch (error) {
        return { error: "Cannot connect to server" };
    }
}


async function calculateFine(vehicle_type, violation, state, vehicle_number) {
    try {
        const response = await fetch(`${BASE_URL}/fine/calculate-fine`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify({ vehicle_type, violation, state, vehicle_number })
        });
        return response.json();

    } catch (error) {
        return { error: "Cannot connect to server" };
    }
}


async function getMyFines() {
    try {
        const response = await fetch(`${BASE_URL}/history/my-history`, {
            headers: {
                "Authorization": `Bearer ${getToken()}`
            }
        });
        return response.json();

    } catch (error) {
        return { error: "Cannot connect to server" };
    }
}


async function generateReceipt(data) {
    try {
        const response = await fetch(`${BASE_URL}/fine/generate-receipt`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${getToken()}`
            },
            body: JSON.stringify(data)
        });
        return response;

    } catch (error) {
        return null;
    }
}
