const id_field = document.getElementById("id_field");
const pass_field = document.getElementById("pass_field");
const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");
const response = document.getElementById("response");
const chars_for_id = "0123456789";
const max_id_length = 12;
const test_pass = "34";

function check_id_syntax(id_input){
    if (id_input === "" || id_input.length !== max_id_length){
        return false;
    }
    for(let i = 0; i < id_input.length; i++){
        if (chars_for_id.includes(id_input[i])){
            continue;
        }
        else{
            return false;
        }
    }
    return true;
}

function check_pass(pass){
    if (pass == test_pass)
        return true;
    else{
        return false;
    }
}

loginBtn.onclick = function(){
    input = id_field.value;
    pass = pass_field.value;
    if(check_id_syntax(input) && check_pass(pass)){
        location.replace("bank-home.html");
    }
    else if(check_id_syntax(input) && !(check_pass(pass))){
        response.textContent = "Mot de passe invalide";
    }
    else if(!(check_id_syntax(input))){
        response.textContent = "ID invalide";
    }
}

