const id_field = document.getElementById("id_field");
const pass_field = document.getElementById("pass_field");
const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const response = document.getElementById("response");
const API_URL = "http://127.0.0.1:8003/api";

async function fetchLogin() {
    const response = await fetch(API_URL + "/login", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: id_field.value,
            password: pass_field.value
        })
    });
    const data = await response.json();
    console.log(data);
    window.location.href = "bank-home.html"
}

loginBtn.onclick = function(){
    fetchLogin(id_field, pass_field);
}

