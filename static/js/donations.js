// let emailValidated = false;
// const emailInput = document.getElementById("id_email");
// var feedback = document.getElementById("feedback-email");
// var emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

// function validateEmail() {
//     event.preventDefault();

//     feedback.innerHTML = "";

//     feedback.classList.add("d-none", "text-danger");
//     var email = emailInput.value;

//     if (!email) {
//         emailValidated = false;
//         feedback.innerHTML = "Entre com um endereço de email.";
//         feedback.classList.remove("d-none");
//        return;
//     }
//     // validate this pattern : [^ @]*@[^ @]*
//     else if (!emailPattern.test(email)) {
//         emailValidated = false;
//         feedback.innerHTML = "Email inválido.";
//         feedback.classList.remove("d-none");
//         return;
//     }

//     // Validating the email

//     feedback.innerHTML = "Email válido.";
//     feedback.classList.remove("d-none", "text-danger");
//     feedback.classList.add("text-success");

//     emailValidated = true;
// }

