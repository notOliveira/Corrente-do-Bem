# Zero Fome

### Leia tudo, mas principalmente as [instruções iniciais](#instruções-iniciais), para que o projeto funcione.

<br>

## Para preparar a inicialização da aplicação

<br>

### Criando ambiente virtual

```
\Zero Fome> python -m venv <name venv>
```

<br>

## Iniciando ambiente virtual

#### Linux

```
\Zero Fome> source venv/bin/activate
```

#### Windows

```
\Zero Fome> .\venv\Scripts\activate
```

<br>

## Desativando ambiente virtual

<br>

```
\Zero Fome> deactivate
```

---

<br>

### Instalando dependências
- Instale na venv preferencialmente

```
(venv) \Zero Fome> pip install -r requirements.txt
```
<br>

---

<br>


## Aplicando as migrações

```
\Zero Fome> python manage.py makemigrations // Provavelmente não será necessário, porque deixarei um arquivo com a migração inicial
\Zero Fome> python manage.py migrate
```

<br>

## Criando super usuário

```
\Zero Fome> python manage.py createsuperuser
```

<br>

## Criando os objetos no banco de dados

- Há um comando para criar os objetos no banco de dados, que deve ser executado após as migrações:

```
\Zero Fome> python manage.py init
```

<br>

## Iniciar o projeto (porta opcional, padrão 8000)


```
\Zero Fome> python manage.py runserver <port>
```

<br>

## Instruções iniciais

- Crie, pelo MySQL Workbench ou Shell uma base de dados previamente, com o nome 'zero_fome'.
- Crie um arquivo chamado [settings_local.py](/zero_fome/zero_fome/settings_local.py) no mesmo diretório do arquivo [settings.py](/zero_fome/zero_fome/settings.py), pois ele contém informações que serão importadas nas configurações, é de extrema importância que o arquivo seja criado. O arquivo criado deve conter as seguintes informações (não foi criado previamente por problemas com o Git):
    ```
    DATABASE_USER = 'root' # Troque por seu usuário na base de dados
    DATABASE_PASSWORD = 'SUA_SENHA_AQUI' # Troque por sua senha na base de dados
    DATABASE_HOST = 'localhost' # Caso esteja utilizando um servidor remoto, troque para o endereço do servidor
    DATABASE_PORT = '3306' # Troque para a porta utilizada pelo servidor de banco de dados
    SECRET_KEY = '?'
    ```
- Como é um arquivo que contém informações potencialmente confidenciais, eu não quero versioná-lo no Git, para não me trazer problemas futuros.

<br>

## Exportando dados

- Exportando dados dos modelos principais (recomendado, por enquanto)
```
\Zero Fome> python -Xutf8 .\manage.py dumpdata main --output=data-models.json
```

- Exportando todos os dados (dá erros de importação, não recomendado)
```
\Zero Fome> python -Xutf8 .\manage.py dumpdata --output=data.json
```

<br>

#### <b>OBS:</b> Os dados estão sendo exportados com o charset adaptado para o Brasil, mas caso queria fazer alguma mudança, retire o argumento -Xutf8.

<br>

## Importando dados

```
\Zero Fome> python manage.py loaddata data.json
```
