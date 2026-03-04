import { useState, useEffect } from "react"
import "./App.css"


// Constantes para a API e opções de status/prioridade
const API = "http://localhost:8000"
const STATUS = ["A Fazer", "Fazendo", "Feito"]
const PRIORIDADES = ["Baixa", "Média", "Alta"]

// Componente principal do aplicativo
function App() {
  const [tasks, setTasks] = useState([]) // Estado para armazenar as tarefas
  const [newTask, setNewTask] = useState({ title: "", description: "", status: "A Fazer", priority: "Baixa" }) // Estado para a nova tarefa

  // useEffect para buscar as tarefas ao carregar o componente
  useEffect(() => {
    // GET para buscar as tarefas no backend
    async function getTasks() {
      const res = await fetch(`${API}/tasks`)
      const data = await res.json()
      setTasks(data)
    }
    getTasks()
  }, [])

  // Função para criar uma nova tarefa
  async function createTask() {
    // POST para criar uma nova tarefa no backend
    try {
    const res = await fetch(`${API}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newTask)
    })
    console.log("status:", res.status) 
    // Recebe a tarefa criada e atualiza o estado
    const created = await res.json()
    setTasks([...tasks, created])
    setNewTask({ title: "", description: "", status: "A Fazer", priority: "Baixa" })
    console.log("Tarefa criada:", created)
   }catch (error) {
      console.error("Erro ao criar tarefa:", error)
    }

  }
  // Função para deletar uma tarefa
  async function deleteTask(id) {
    // DELETE para remover a tarefa do backend
    await fetch(`${API}/tasks/${id}`, { method: "DELETE" })
    setTasks(tasks.filter((task) => task.id !== id))
    console.log("Tarefa deletada:", id)
  }
  // Função para atualizar uma tarefa (ex: mudar status)
  async function updateTask(id, updatedTask) {
    const res = await fetch(`${API}/tasks/${id}`, { // PATCH para atualizar a tarefa no backend
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updatedTask)
    })
    // Recebe a tarefa atualizada e atualiza o estado
    const updated = await res.json()
    setTasks(tasks.map((task) => task.id === id ? updated : task))
    console.log("Tarefa atualizada:", updated)
  }

  // Renderização do componente com formulário para criar tarefas e colunas do Kanban
  return (
    <div className="App">
      <h1 className="kanban-title">Kanban Board</h1>

      {/* Formulário para criar nova tarefa */}
      <div className="form">
        <input
          placeholder="Título"
          value={newTask.title}
          onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
        />
        <input
          placeholder="Descrição"
          value={newTask.description}
          onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
        />
        <select
          value={newTask.status}
          onChange={(e) => setNewTask({ ...newTask, status: e.target.value })}
        >
          {STATUS.map((col) => <option key={col} value={col}>{col}</option>)}
        </select>
        <select
          value={newTask.priority}
          onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
        >
          {PRIORIDADES.map((prio) => <option key={prio} value={prio}>{prio}</option>)}
        </select>
        <button onClick={createTask}>Criar tarefa</button>
      </div>

      {/* Colunas do Kanban para cada status */}
      <div className="kanban">
        {STATUS.map((coluna) => (
          <div key={coluna} className="coluna">
            <h2>{coluna}</h2>
            {/* Iterando sobre as tarefas para exibir apenas as que correspondem ao status da coluna */}
            {tasks
              .filter((task) => task.status === coluna)
              .map((task) => (
                <div key={task.id} className={`card prioridade-${task.priority.toLowerCase()}`}>
                  <p className="card-title">{task.title}</p>
                  {task.description && <p className="card-desc">{task.description}</p>}
                  <span className={`badge ${task.priority.toLowerCase()}`}>{task.priority}</span>
                  <div className="card-actions">
                    {/* Botão para mover a tarefa para o próximo status, exceto se já estiver na coluna "Feito" */}
                    {coluna !== "Feito" && (
                      <button onClick={() => updateTask(task.id, { ...task, status: coluna === "A Fazer" ? "Fazendo" : "Feito" })}>
                        Avançar →
                      </button>
                    )}
                    {/* Botão para deletar a tarefa */}
                    <button className="btn-delete" onClick={() => deleteTask(task.id)}>Deletar</button>
                  </div>
                </div>
              ))}
          </div>
        ))}
      </div>
    </div>
  )
}

export default App