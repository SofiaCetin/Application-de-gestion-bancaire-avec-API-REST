const user_wallet = document.getElementById("balance");
const API_URL = "http://127.0.0.1:8000/api";
const user_names = document.getElementById("user_names");
const user_id = document.getElementById("user_id");

async function fetchBalance(){
    const response = await fetch(API_URL + "/balance", {
        method: "GET",
        credentials: "include"
        });
    
    if (response.status == 200){
        const data = await response.json();
        const balance = data.balance;
        user_wallet.textContent = balance + " €";
    }
    else{
        return null;
    }

}

async function fetchUserInfo(){
    const response = await fetch(API_URL + "/user-info", {
        method: "GET",
        credentials: "include"
        });
    
    if (response.status == 200){
        const data = await response.json();
        const first_name = data.first;
        const last_name = data.last;
        user_names.textContent = first_name + " " + last_name;
    }
    else{
        return null;
    }
} 

async function isLogged(){
    const response = await fetch(API_URL + "/logged-user", {
        method: "GET",
        credentials: "include"
        });
    
    if (response.status == 200){
        const data = await response.json();
        const userId = data.user_id;
        user_id.textContent = userId;
        return true;
    }
    else{
        return false;
    }
}

async function init(){
    logged = await isLogged();
    if (logged){
        fetchBalance();
        fetchUserInfo();
    }
    else{
        window.location.href = "login.html";
    }
}

init();