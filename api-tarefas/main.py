"""API REST simples de lista de tarefas (FastAPI + SQLite)."""
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB = "tarefas.db"
app = FastAPI(title="API de Tarefas")


def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela():
    with conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                concluida INTEGER NOT NULL DEFAULT 0
            )
            """
        )


criar_tabela()


class TarefaNova(BaseModel):
    titulo: str


class TarefaAtualiza(BaseModel):
    titulo: str | None = None
    concluida: bool | None = None


def para_dict(linha):
    return {"id": linha["id"], "titulo": linha["titulo"], "concluida": bool(linha["concluida"])}


@app.get("/tarefas")
def listar():
    with conectar() as conn:
        linhas = conn.execute("SELECT * FROM tarefas ORDER BY id").fetchall()
    return [para_dict(l) for l in linhas]


@app.post("/tarefas", status_code=201)
def criar(tarefa: TarefaNova):
    with conectar() as conn:
        cur = conn.execute("INSERT INTO tarefas (titulo) VALUES (?)", (tarefa.titulo,))
        linha = conn.execute("SELECT * FROM tarefas WHERE id = ?", (cur.lastrowid,)).fetchone()
    return para_dict(linha)


@app.get("/tarefas/{tarefa_id}")
def buscar(tarefa_id: int):
    with conectar() as conn:
        linha = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    if linha is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return para_dict(linha)


@app.put("/tarefas/{tarefa_id}")
def atualizar(tarefa_id: int, dados: TarefaAtualiza):
    with conectar() as conn:
        linha = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
        if linha is None:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        titulo = dados.titulo if dados.titulo is not None else linha["titulo"]
        concluida = int(dados.concluida) if dados.concluida is not None else linha["concluida"]
        conn.execute(
            "UPDATE tarefas SET titulo = ?, concluida = ? WHERE id = ?",
            (titulo, concluida, tarefa_id),
        )
        nova = conn.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    return para_dict(nova)


@app.delete("/tarefas/{tarefa_id}", status_code=204)
def remover(tarefa_id: int):
    with conectar() as conn:
        cur = conn.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
