# =============================
# Testes para o backend do Kanban Board
# =============================


import pytest
from main import Task
from main import db_connect, startup_event, get_tasks, create_task, update_task, delete_task

# ========================================
#           TESTES UNITÁRIOS
# =======================================

# Testando a classe Task para garantir que os valores padrão estão corretos
def test_task_com_valores_padrao():
    task = Task(title="Estudar")
    assert task.status == "A Fazer"
    assert task.priority == "Baixa"

# Testando a classe Task para garantir que os valores estão sendo atribuídos corretamente
def test_task_com_valores():
    task = Task(title="Estudar", status="Fazendo", priority="Alta")
    assert task.title == "Estudar"
    assert task.description == None
    assert task.status == "Fazendo"
    assert task.priority == "Alta"

# Testando a classe Task com titulo vazio para garantir que o campo obrigatório está sendo validado
def test_task_titulo_vazio():
    with pytest.raises(ValueError):
        Task(title="")

# Testando a classe Task com o titulo None para garantir que o campo obrigatório está sendo validado
def test_task_titulo_none():
    with pytest.raises(ValueError):
        Task(title=None)


# ========================================
#           TESTES DE INTEGRAÇÃO
# ========================================


# Testando a conexão com o banco de dados (pode e deve ser feito utilizando um mock ou um banco de teste para evitar afetar os dados reais)
def test_db_connect():
    conn = db_connect()
    assert conn is not None
    conn.close()

# Testando criaçao da tabela de tarefas no banco de dados
def test_startup_event():
    startup_event()
# Testando a criação de uma nova tarefa no banco de dados
def test_create_task():
    task = Task(title="Testar API", description="Criar testes para a API", status="A Fazer", priority="Média")
    new_task = create_task(task)
    assert new_task is not None
    assert new_task['title'] == "Testar API"
    assert new_task['description'] == "Criar testes para a API"
    assert new_task['status'] == "A Fazer"
    assert new_task['priority'] == "Média"

# Testando a criação de uma tarefa com título vazio para garantir que a validação está funcionando
def test_create_task_titulo_vazio():
    # Diferentemente de testar a classe Task diretamente, aqui estamos testando a função create_task para garantir
    #  que a validação do título vazio está sendo aplicada corretamente quando tentamos criar uma tarefa no banco de dados
    with pytest.raises(ValueError):
        create_task(Task(title="", description="Descrição da tarefa", status="A Fazer", priority="Baixa"))

# Testando a obtenção de todas as tarefas do banco de dados
def test_get_tasks():
    tasks = get_tasks()
    assert isinstance(tasks, list)

# Testando banco vazio para garantir que a função get_tasks retorna uma lista vazia
def test_get_tasks_banco_vazio():
    # Limpar a tabela de tarefas para garantir que o banco esteja vazio
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    cursor.close()
    conn.close()

    # Retorno deve ser uma lista e a lista deve estar vazia
    tasks = get_tasks()
    assert isinstance(tasks, list)
    assert len(tasks) == 0

# Testando a atualização de uma tarefa no banco de dados
def test_update_task():
    # Criar uma tarefa para atualizar
    task = Task(title="Tarefa para atualizar", description="Descrição da tarefa", status="A Fazer", priority="Baixa")
    new_task = create_task(task)
    task_id = new_task['id']
    
    # Atualizar a tarefa
    updated_task = update_task(task_id, Task(title="Tarefa atualizada", description="Descrição atualizada", status="Fazendo", priority="Alta"))
    
    assert updated_task is not None
    assert updated_task['title'] == "Tarefa atualizada"
    assert updated_task['description'] == "Descrição atualizada"
    assert updated_task['status'] == "Fazendo"
    assert updated_task['priority'] == "Alta"

# Testando a atualização de uma tarefa com id inexistente para garantir que a função update_task lida corretamente com esse cenário
def test_update_task_id_inexistente():
    with pytest.raises(ValueError):
        update_task(9999, Task(title="Tarefa inexistente", description="Descrição da tarefa", status="A Fazer", priority="Baixa"))


# Testando a exclusão de uma tarefa no banco de dados
def test_delete_task():
    # Criar uma tarefa para excluir
    task = Task(title="Tarefa para excluir", description="Descrição da tarefa", status="A Fazer", priority="Baixa")
    new_task = create_task(task)
    task_id = new_task['id']
    
    # Excluir a tarefa
    task_deleted = delete_task(task_id)
    
    # Verificar se a tarefa foi excluída
    tasks = get_tasks()
    assert all(t['id'] != task_id for t in tasks)
    assert task_deleted['message'] == f"Tarefa deletada com ID {task_id}"


# Testando exclusão de uma tarefa com id inexistente para garantir que a função delete_task lida corretamente com esse cenário
def test_delete_task_id_inexistente():
    with pytest.raises(ValueError):
        delete_task(9999)






