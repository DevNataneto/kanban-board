# Documentação de Testes — Kanban Board

## Descrição do Sistema

Sistema de gerenciamento de tarefas no formato Kanban.
O usuário pode criar, mover entre colunas e deletar tarefas.
Cada tarefa possui título, descrição, status e prioridade.

---

## Backend

### Endpoints
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /tasks | Lista todas as tarefas |
| POST | /tasks | Cria uma nova tarefa |
| PATCH | /tasks/{id} | Atualiza uma tarefa |
| DELETE | /tasks/{id} | Deleta uma tarefa |

### Regras de negócio
- Status válidos: `A Fazer`, `Fazendo`, `Feito`
- Prioridades válidas: `Baixa`, `Média`, `Alta`
- Título é obrigatório
- Descrição é opcional

---

## Testes Unitários — Backend

### `status_valido()`
| Caso | Entrada | Esperado |
|------|---------|----------|
| ✅ status válido | `"A Fazer"` | `True` |
| ✅ status válido | `"Fazendo"` | `True` |
| ✅ status válido | `"Feito"` | `True` |
| ❌ status inválido | `"Pendente"` | `False` |
| 🔲 string vazia | `""` | `False` |

### `prioridade_valida()`
| Caso | Entrada | Esperado |
|------|---------|----------|
| ✅ prioridade válida | `"Alta"` | `True` |
| ✅ prioridade válida | `"Média"` | `True` |
| ✅ prioridade válida | `"Baixa"` | `True` |
| ❌ prioridade inválida | `"Urgente"` | `False` |
| 🔲 string vazia | `""` | `False` |

---

## Testes Unitários — Frontend

### `createTask()`
| Caso | Entrada | Esperado |
|------|---------|----------|
| ✅ tarefa válida | título preenchido | tarefa aparece na coluna correta |
| ❌ título vazio | título `""` | botão não deve criar |

---

## Testes de Integração

### POST /tasks
| Caso | Entrada | Esperado |
|------|---------|----------|
| ✅ dados válidos | título + status + prioridade válidos | retorna tarefa com id gerado |
| ❌ título vazio | `title: ""` | retorna erro 400 |
| ❌ prioridade inválida | `priority: "Urgente"` | retorna erro 400 |

### GET /tasks
| Caso | Esperado |
|------|----------|
| ✅ banco com tarefas | retorna lista de tarefas |
| ✅ banco vazio | retorna lista vazia `[]` |

---

## Testes E2E — Playwright

### Fluxo criar tarefa
1. Acessar `http://localhost:5173`
2. Preencher título
3. Selecionar status e prioridade
4. Clicar em "Criar tarefa"
5. Verificar se apareceu na coluna correta

### Fluxo avançar tarefa
1. Criar tarefa em "A Fazer"
2. Clicar em "Avançar →"
3. Verificar se moveu para "Fazendo"

### Fluxo deletar tarefa
1. Clicar em "Deletar"
2. Verificar se sumiu da tela