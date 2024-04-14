const emailInput = document.getElementsByClassName('email-input')[0];
const emailDiv = document.getElementById('email-div');
const addButton = document.getElementById('add-email');

addButton.addEventListener('click', () => {
    var emailInputGroup = document.createElement('div');
    emailInputGroup.className = 'input-group mb-3';
    emailInputGroup.innerHTML = `
        <input type="text" class="form-control" name="email" placeholder="fulano@email.com">
        <span class="btn input-group-text bg-danger remove-input">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"></path>
                <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"></path>
            </svg>
        </span>
    `;
    emailDiv.appendChild(emailInputGroup);
    
    // Atualize a lista de botões de remoção
    let removeButtons = document.getElementsByClassName('remove-input');
    
    // Crie um listener para cada botão de remoção
    for (let i = 0; i < removeButtons.length; i++) {
        removeButtons[i].addEventListener('click', function() {
            this.parentNode.remove(); // Isso remove o elemento pai do botão clicado
        });
    }
});
