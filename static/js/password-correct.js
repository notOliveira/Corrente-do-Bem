const passwordCheck = document.getElementById('password-check');
const passwordInput1 = document.getElementById('password1');
const passwordInput2 = document.getElementById('password2');
const submitButton = document.getElementById('create-account');

// Regex para validar senha: deve conter 8 dígitos ou mais, envolvendo números e pelo menos um caractere especial
const regex = /^(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;

function validatePassword() {
    submitButton.disabled = true;
    passwordCheck.classList = "";
    passwordCheck.innerHTML = "";

    // p1 ou p2 fora das regras
    if ((regex.test(passwordInput1.value) || regex.test(passwordInput2.value)) == false) {
        passwordCheck.classList.add("text-danger");
        passwordCheck.innerHTML = "A senha deve conter 8 dígitos ou mais, envolvendo números e pelo menos um caractere especial";
    }
    // p1 != p2 = senhas diferem
    else if (passwordInput1.value != passwordInput2.value) {
        passwordCheck.classList.add("text-warning");
        passwordCheck.innerHTML = "As senhas devem ser iguais";
    }
    // senhas corretas
    else {
        passwordCheck.classList.add("text-success");
        passwordCheck.innerHTML = "As senhas estão coincidem e estão corretas";
        submitButton.disabled = false;
    }
}

passwordInput1.addEventListener('input', validatePassword);
passwordInput2.addEventListener('input', validatePassword);