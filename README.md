# 🏋️‍♂️ WorkoutAPI — FastAPI + Async + PostgreSQL

API assíncrona desenvolvida com **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **Alembic** e **fastapi-pagination** para gerenciar atletas, categorias e centros de treinamento em uma competição de CrossFit.  

Este projeto foi desenvolvido como desafio do curso da **DIO (Digital Innovation One)** e faz parte do meu portfólio como desenvolvedor Back-End com Python.

---

# 🚀 Tecnologias utilizadas

| Tecnologia | Função |
|-----------|--------|
| **Python 3.11+** | Linguagem |
| **FastAPI** | Framework web assíncrono |
| **SQLAlchemy 2.0** | ORM para interação com o banco |
| **Asyncpg** | Driver assíncrono PostgreSQL |
| **Alembic** | Migrações do banco de dados |
| **Pydantic** | Validação de dados |
| **Uvicorn** | Servidor ASGI |
| **fastapi-pagination** | Paginação automática |

---

# 📌 Descrição do Projeto

O objetivo é construir uma API moderna e eficiente que permita:

- Cadastrar atletas
- Registrar centros de treinamento
- Criar categorias
- Listar atletas com filtros inteligentes
- Tratar exceções de forma profissional
- Paginar resultados automaticamente

A API foi construída com **arquitetura modular**, seguindo boas práticas de mercado e organização limpa.

---

# 🎯 Funcionalidades Implementadas (Desafio DIO)

### ✔ 1. Query Parameters em `/atletas`
Permite filtrar atletas por:
- `nome`
- `cpf`

Exemplo: 
/atletas?nome=joao /atletas?cpf=12345678900

### ✔ 2. Customização do Response
O endpoint **GET /atletas** retorna:

- nome  
- categoria  
- centro_treinamento  

Exemplo de retorno:
```json
{
  "nome": "João Silva",
  "categoria": "RX",
  "centro_treinamento": "CT Fortaleza"
}
