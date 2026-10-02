# API de Tarefas

API REST simples para gerenciar uma lista de tarefas, feita para praticar back-end e SQL. Permite criar, listar, buscar, atualizar e remover tarefas, salvas em um banco SQLite.

## Tecnologias
Python 3, FastAPI, SQLite (módulo `sqlite3` da biblioteca padrão).

## Como executar
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
A API sobe em `http://127.0.0.1:8000`. A documentação interativa fica em `http://127.0.0.1:8000/docs`.

## Endpoints
| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/tarefas` | Lista todas as tarefas |
| POST | `/tarefas` | Cria uma tarefa (`{"titulo": "Estudar SQL"}`) |
| GET | `/tarefas/{id}` | Busca uma tarefa |
| PUT | `/tarefas/{id}` | Atualiza título e/ou status (`{"concluida": true}`) |
| DELETE | `/tarefas/{id}` | Remove uma tarefa |

## Exemplo
```bash
curl -X POST http://127.0.0.1:8000/tarefas -H "Content-Type: application/json" -d '{"titulo": "Estudar SQL"}'
curl http://127.0.0.1:8000/tarefas
```

## Próximos passos
- Testes automatizados com `pytest`
- Autenticação de usuários
- Trocar SQLite por PostgreSQL

## Autor
João Felipe — [GitHub](https://github.com/jotalipe33)
