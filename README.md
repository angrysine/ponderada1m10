# ponderada1m10

Essa ponderada tem uma api de uma todo list, onde é possível adicionar, deletar, editar e listar tarefas, além de criar usuaŕios.

## Instalação

Para instalar as dependências do projeto, execute o comando:

```bash
pip install -r requirements.txt
```

## Execução

Para executar o projeto, execute o comando:

```bash
docker compose up
```

O swagger da api estará disponível em `http://localhost:5000/swagger`

O projeto contem uma coleção do insomnia para testar a api, disponível em `insomniaDoc.json`, para usar as rotas no swagger deve se clicar  no cadeado no canto superior direito da tela e inserir "bearer token", substituindo "token" pelo token gerado ao criar um usuário. Se usar a coleção do insomnia, deve se passar no header o valor do token.

## Video

Segue aqui um video demonstração do funcionamento da aplicação: [Video](https://youtu.be/lw6sFVI_TJc)
