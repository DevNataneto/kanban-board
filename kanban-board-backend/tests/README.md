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

### `Task` (classe)
| Caso | Entrada | Esperado |
|------|---------|----------|
| ✅ valores padrão | `Task(title="Estudar")` | `status="A Fazer"`, `priority="Baixa"`, `description=None` |
| ✅ campos preenchidos | `Task(title="Estudar", status="Fazendo", priority="Alta")` | retorna objeto com os valores informados |
| ❌ título ausente | `Task()` | erro de validação do Pydantic |

---

## Testes de Integração — Backend

### `db_connect()`
| Caso | Esperado |
|------|----------|
| ✅ banco rodando | retorna objeto de conexão válido |

### `GET /tasks`
| Caso | Esperado |
|------|----------|
| ✅ banco com tarefas | retorna lista de tarefas |
| ✅ banco vazio | retorna lista vazia `[]` |

### `POST /tasks`
| Caso | Entrada | Esperado |
|------|---------|----------|
| ✅ dados válidos | título + status + prioridade válidos | retorna tarefa com `id` gerado pelo banco |
| ❌ título vazio | `title: ""` | erro de validação |

### `PATCH /tasks/{id}`
| Caso | Entrada | Esperado |
|------|---------|----------|
| ✅ atualização válida | `id` existente + novos dados | retorna tarefa atualizada |
| ❌ id inexistente | `id` que não existe no banco | retorna erro |

### `DELETE /tasks/{id}`
| Caso | Entrada | Esperado |
|------|---------|----------|
| ✅ id existente | `id` de tarefa existente | retorna mensagem de confirmação |
| ❌ id inexistente | `id` que não existe no banco | retorna erro |

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
