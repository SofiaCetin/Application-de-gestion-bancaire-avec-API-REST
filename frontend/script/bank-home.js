const user_wallet = 0;
const user_id = undefined;
const API_URL = "http://127.0.0.1:8003/api";
const welcome_msg = document.getElementById("welcome_msg");
const id_msg = document.getElementById("id_msg");

function init_msg(user_id){
    welcome_msg.textContent = `Connecté en tant que: ${user_id}`;
    id_msg.textContent = `ID: ${user_id}`;
}

async function fetchBalance(){
    const response = await fetch(API_URL + "/balance", {
        method: "GET",
        credentials: "include"
        });

    const data = await response.json();
    console.log(data);

}

init_msg(user_id);
fetchBalance();