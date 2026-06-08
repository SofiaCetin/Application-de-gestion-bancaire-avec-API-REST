const id_field = document.getElementById("id_field");
const pass_field = document.getElementById("pass_field");
const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const message = document.getElementById("response");
const API_URL = "http://127.0.0.1:8000/api";

async function fetchLogin() {
    try{
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

        if (response.status === 200){
            window.location.href = "solde.html";
        }
        else{
            id_field.value = "";
            pass_field.value = "";
            message.textContent = "Identifiant ou mot de passe invalide";
        }
    }
    catch(error){
        response.textContent = "Serveur inaccessible";
    }
}

async function isLogged(){
    const response = await fetch(API_URL + "/logged-user", {
        method: "GET",
        credentials: "include"
        });

    if (response.status == 200){
        return true;
    }
    else{
        return false;
    }
}

async function init(){
    logged = await isLogged();
    if (logged){
        window.location.href = "solde.html"
    }
    else{
        loginBtn.onclick = function(){
        fetchLogin(id_field, pass_field);
        }
    }
}

init();

