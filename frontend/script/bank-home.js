const user_wallet = 0;
const user_last = "TEST";
const user_first = "Test";
const user_id = "123456789012";
const welcome_msg = document.getElementById("welcome_msg");
const id_msg = document.getElementById("id_msg");

function init_msg(user_first, user_last){
    welcome_msg.textContent = `Connecté en tant que: ${user_first} ${user_last}`;
    id_msg.textContent = `ID: ${user_id}`;
}

init_msg(user_first, user_last);