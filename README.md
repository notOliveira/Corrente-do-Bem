# Corrente do Bem

### Leia tudo, mas principalmente as [instruções iniciais](#instruções-iniciais), para que o projeto funcione.

<br>

## Para preparar a inicialização da aplicação

<br>

### Criando ambiente virtual

```
\> python -m venv <name venv>
```

<br>

## Iniciando ambiente virtual

#### Linux

```
\> source venv/bin/activate
```

#### Windows

```
\> .\venv\Scripts\activate
```

<br>

## Desativando ambiente virtual

<br>

```
\> deactivate
```

---

<br>

### Instalando dependências
- Instale na venv preferencialmente

```
(venv) \> pip install -r requirements.txt
```
<br>

---

<br>


## Aplicando as migrações

```
\> python manage.py makemigrations // Provavelmente não será necessário, porque deixarei um arquivo com a migração inicial
\> python manage.py migrate
```

<br>

## Criando super usuário

```
\> python manage.py createsuperuser
```

<br>

## Criando os objetos no banco de dados

- Há um comando para criar os objetos no banco de dados, que deve ser executado após as migrações:

```
\> python manage.py init
```

<br>

## Iniciar o projeto (porta opcional, padrão 8000)


```
\> python manage.py runserver <port>
```

<br>

## Instruções iniciais

- Crie, pelo MySQL Workbench ou Shell uma base de dados previamente, com o nome 'corrente_do_bem'.
- Crie um arquivo chamado [.env](/.env), pois ele contém informações que serão importadas nas configurações, é de extrema importância que o arquivo seja criado. O arquivo criado deve conter as seguintes informações:
    ```
    DEVENV=development # Essa configuração serve para definir o ambiente (local), mas caso não queira configuar uma base de dados, mude para 'sqlite'
    LOCALDATABASE = 'root' # Troque por seu usuário na base de dados
    LOCALPASSWORD = 'SUA_SENHA_AQUI' # Troque por sua senha na base de dados
    LOCALHOST = 'localhost' # Caso esteja utilizando um servidor remoto, troque para o endereço do servidor
    LOCALPORT = '3306' # Troque para a porta utilizada pelo servidor de banco de dados
    GOOGLE_API_KEY='?' # Coloque sua chave do Google API
    SECRET_KEY = '?'
    ALLOWED_HOSTS=localhost # Para adicionar mais, coloque um ';' após o 'localhost'
    CSRF_TRUSTED_ORIGINS=https://corrente-do-bem.up.railway.app
    CORS_ALLOWED_ORIGINS=https://corrente-do-bem.up.railway.app;*

    ```
- Como é um arquivo que contém informações potencialmente confidenciais, eu não quero versioná-lo no Git, para não me trazer problemas futuros.

<br>

## Exportando dados

- Exportando dados dos modelos principais (recomendado, por enquanto)
```
\> python -Xutf8 .\manage.py dumpdata main --output=data-models.json
```

- Exportando todos os dados (dá erros de importação, não recomendado)
```
\> python -Xutf8 .\manage.py dumpdata --output=data.json
```

<br>

#### <b>OBS:</b> Os dados estão sendo exportados com o charset adaptado para o Brasil, mas caso queria fazer alguma mudança, retire o argumento -Xutf8.

<br>

## Importando dados

```
\> python manage.py loaddata data.json
```
