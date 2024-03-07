# Mães Solidárias API

## Configuração e Execução do Projeto Django REST

Este guia fornece instruções passo a passo sobre como configurar e executar um projeto Django REST. Certifique-se de seguir cada etapa cuidadosamente para garantir uma configuração bem-sucedida.

### Pré-requisitos

Antes de começar, certifique-se de ter os seguintes pré-requisitos instalados em seu sistema:

- Python 3.x
- pip (gerenciador de pacotes Python)

### Configuração do Ambiente Virtual

1. Abra o terminal na raiz do projeto.

2. Crie um ambiente virtual utilizando o comando:

    ```bash
    python -m venv venv
    ```

3. Ative o ambiente virtual:

    - No Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - No macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

### Instalação das Dependências

1. Certifique-se de que o ambiente virtual está ativado.

2. Instale as dependências do projeto utilizando o comando:

    ```bash
    pip install -r requirements.txt
    ```

## Configuração do Banco de Dados

1. Abra o arquivo `settings.py` na pasta do seu projeto.

2. Encontre a seção de configuração do banco de dados e ajuste as configurações conforme necessário (por exemplo, nome do banco de dados, usuário, senha).

3. Execute as migrações para criar as tabelas do banco de dados:

    ```bash
    python manage.py migrate
    ```

### Executando o Servidor

1. No terminal, execute o seguinte comando para iniciar o servidor de desenvolvimento:

    ```bash
    python manage.py runserver
    ```

2. Abra o navegador e acesse `http://127.0.0.1:8000/` para verificar se o servidor está funcionando corretamente.

### Testando a API

1. Utilize ferramentas como [Postman](https://www.postman.com/) ou [curl](https://curl.se/) para testar as diferentes endpoints da sua API.

## Documentação

Acesse a documentação das rotas em `http://127.0.0.1:8000/doc/`

