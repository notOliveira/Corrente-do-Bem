// CEP Mask

const handleZipCode = (event) => {
    let input = event.target
    input.value = zipCodeMask(input.value)
}
  
const zipCodeMask = (value) => {
    if (!value) {
        return ""
    }
    value = value.replace(/\D/g,'')
    value = value.replace(/(\d{5})(\d)/,'$1-$2')
    return value
}

const handlePhone = (event) => {
    let input = event.target
    input.value = phoneMask(input.value)
}

const phoneMask = (value) => {
    if (!value) {
        return ""
    }
    value = value.replace(/\D/g,'')
    return value
}

function getCep() {
    event.preventDefault(); // Prevenir o comportamento padrão do formulário

    // Obter o valor do CEP do campo de entrada
    let cep = document.getElementById('id_cep').value;
    let feedback = document.getElementById('feedback-cep');
    let street = document.getElementById('id_street');
    let neighborhood = document.getElementById('id_neighborhood');
    let city = document.getElementById('id_city');
    let state = document.getElementById('id_state');

    // Limpar os campos de endereço e feedback
    street.value = '';
    neighborhood.value = '';
    city.value = '';
    state.value = '';
    feedback.innerHTML = '';
    feedback.classList.add('d-none');

    // Verificar se o CEP tem o formato correto (9 caracteres)
    if (!cep) {
        feedback.classList.remove('d-none');
        feedback.innerHTML = 'Insira um CEP!';
        return;
    } else if (cep.length !== 9) {
        console.error('CEP inválido');
        feedback.classList.remove('d-none');
        feedback.innerHTML = 'CEP inválido!';
        return;
    }

    // Construir a URL da API do ViaCEP
    var url = 'https://viacep.com.br/ws/' + cep + '/json/';

    // Fazer a requisição para a API do ViaCEP
    fetch(url)
        .then(response => {
            // Verificar se a resposta da requisição foi bem-sucedida
            if (!response.ok) {
                feedback.classList.remove('d-none');
                feedback.innerHTML = 'Erro ao obter dados do CEP.';
                throw new Error('Erro ao obter dados do CEP');
            }
            return response.json();
        })
        .then(data => {
            // Verificar se a API retornou um erro
            if (data.erro) {
                feedback.classList.remove('d-none');
                feedback.innerHTML = 'CEP não encontrado!';
                return;
            }
            
            // Atualizar os campos de endereço com os dados recebidos da API
            street.value = data.logradouro || '';
            neighborhood.value = data.bairro || '';
            city.value = data.localidade || '';
            state.value = data.uf || '';
        })
        .catch(error => {
            feedback.classList.remove('d-none');
            feedback.innerHTML = 'Erro ao processar a requisição';
            console.error('Erro ao processar a requisição:', error);
        });
}

