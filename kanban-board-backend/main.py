from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
from pydantic import BaseModel
from typing import Optional


# Criando a aplicação FastAPI
app = FastAPI()

# Configurando o CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definindo o modelo de dados para uma tarefa usando Pydantic para validação de dados
# (Sem isso o FastAPI não consegue validar os dados recebidos e pode causar erros)
class Task(BaseModel):
    title: str
    description: Optional[str] = None # Campo opcional para descrição da tarefa
    status: str = "Pendente"
    priority: str = "Baixa"

# Função para conectar ao banco de dados PostgreSQL
def db_connect():
    # Conectando ao banco de dados PostgreSQL
    conn = psycopg2.connect(
        host="localhost",
        database="kanban-board",
        user="postgres",
        password="admin"
    )
    return conn

# Evento de inicialização para criar a tabela "tasks" se ela não existir
@app.on_event("startup")
def startup_event():
    # Criando a tabela "tasks" se ela não existir
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'Pendente',
            priority TEXT NOT NULL DEFAULT 'Baixa'
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Endpoint para obter todas as tarefas do banco de dados
@app.get("/tasks")
def get_tasks():
    conn = db_connect()
    # Usando RealDictCursor para obter os resultados como dicionários para facilitar a conversão para JSON
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) 
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return list(tasks)

# Endpoint para criar uma nova tarefa no banco de dados
@app.post("/tasks")
def create_task(task: Task):
    conn = db_connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    # Inserindo a nova tarefa no banco de dados e retornando a tarefa criada como dicionário
    cursor.execute(
        "INSERT INTO tasks (title, description, status, priority) VALUES (%s, %s, %s, %s) RETURNING *",
        (task.title, task.description, task.status, task.priority)
    )
    new_task = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return dict(new_task)

# Endpoint para atualizar uma tarefa existente no banco de dados
@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    conn = db_connect()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        "UPDATE tasks SET title=%s, description=%s, status=%s, priority=%s WHERE id=%s RETURNING *",
        (task.title, task.description, task.status, task.priority, task_id)
    )
    updated_task = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return dict(updated_task)

# Endpoint para deletar uma tarefa do banco de dados
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": f"Tarefa deletada com ID {task_id}"}