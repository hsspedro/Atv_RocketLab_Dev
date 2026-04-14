# 🚀 Atv_RocketLab_Dev

Aplicação fullstack desenvolvida com foco em simular um ambiente de e-commerce moderno, utilizando **FastAPI no backend** e **React + Vite no frontend**.

---

## 📌 Funcionalidades

- Cadastro de produtos  
- Listagem e busca de produtos  
- Sistema de avaliações por produto  
- Integração com banco de dados  
- API REST com FastAPI  
- Interface com React + TailwindCSS  

---

## 🏗️ Estrutura do Projeto

```
Atv_RocketLab_Dev/
│
├── backend/     # API FastAPI
├── frontend/    # Aplicação React
└── README.md
```

---

## 🧠 Tecnologias

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite

### Frontend
- React
- Vite
- TypeScript
- TailwindCSS

---

## ⚙️ Como Executar

### 🔧 Backend

```bash
cd backend
python -m venv venv
```

Ativar ambiente:

**Windows**
```bash
venv\Scripts\activate
```

**Linux/Mac**
```bash
source venv/bin/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Copulando a base de dados:
```bash
python -m app.utils.load_csv

python -m app.utils.fix_media

python -m app.utils.atualizar_precos
```


```bash
pip install -r requirements.txt
```
Rodar servidor:

```bash
uvicorn app.main:app --reload
```

Acesse:
- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  

---

### 🎨 Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse:
- http://localhost:5173  

---

## 🗄️ Banco de Dados

- SQLite por padrão  
- Criação automática das tabelas  
- Suporte a ingestão via CSV  

---

## 🔄 Endpoints

### Produtos
- `GET /produtos`
- `POST /produtos`

### Avaliações
- `GET /produto/{id}/avaliacoes`

---

## 📁 Estrutura Backend

```
backend/app/
│
├── models/
├── schemas/
├── routers/
├── services/
├── utils/
└── main.py
```

---

## 🧪 Testes

```bash
pytest
```

---

## 💡 Melhorias Futuras

- Autenticação com JWT  
- Sistema completo de pedidos  
- Deploy em nuvem  
- Testes automatizados mais robustos  
- Paginação e filtros  

---

## 👨‍💻 Autor

Pedro Henrique  
https://github.com/hsspedro  

---

## 📄 Licença

Uso acadêmico.
