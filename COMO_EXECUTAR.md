# 🚀 Guia Rápido de Execução — CloudPulse

Este documento contém o passo a passo direto para compilar, executar e testar o projeto no seu computador ou no do professor.

---

## ⚡ Método 1: Executando com Docker (Recomendado para o Trabalho)

> **Pré-requisito:** Certifique-se de que o **Docker Desktop** esteja aberto e rodando no seu computador.

### 1. Construir a imagem Docker
No terminal dentro da pasta do projeto, execute:
```bash
docker build -t cloudpulse-backend:1.0 .
```

### 2. Rodar o contêiner
```bash
docker run -d -p 8000:8000 --name cloudpulse_app cloudpulse-backend:1.0
```

### 3. Acessar a aplicação no navegador
- 🌐 **Dashboard & Aplicação:** [http://localhost:8000](http://localhost:8000)
- 📘 **Página de Teoria Acadêmica:** [http://localhost:8000/teoria/](http://localhost:8000/teoria/)
- 📡 **API JSON de Diagnóstico:** [http://localhost:8000/api/system-info/](http://localhost:8000/api/system-info/)

### 4. Comandos para demonstrar ao professor
```bash
# Ver o contêiner ativo e a porta mapeada (0.0.0.0:8000->8000/tcp)
docker ps

# Ver os logs do Django e Gunicorn gerados dentro do contêiner
docker logs cloudpulse_app

# Entrar no contêiner para provar que é Linux Debian com isolamento
docker exec -it cloudpulse_app bash
# (dentro do contêiner, digite 'hostname' ou 'uname -a' e depois 'exit' para sair)

# Para parar e remover o contêiner após a apresentação:
docker stop cloudpulse_app
docker rm cloudpulse_app
```

---

## 📦 Método 2: Executando com Docker Compose

Se preferir usar o `docker compose` (com volume persistente para não perder dados ao reiniciar):

```bash
# Subir a aplicação em segundo plano
docker compose up --build -d

# Visualizar logs em tempo real
docker compose logs -f

# Parar a aplicação
docker compose down
```

---

## 💻 Método 3: Executando Localmente (Sem Docker)

Se precisar rodar diretamente no Python:

### Windows (PowerShell)
```powershell
# 1. Ativar o ambiente virtual já configurado
.\.venv\Scripts\Activate.ps1

# 2. Aplicar migrações do banco de dados (se necessário)
python manage.py migrate

# 3. Popular dados demonstrativos
python manage.py seed_data

# 4. Iniciar o servidor
python manage.py runserver 8000
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Como rodar os testes automatizados
```bash
python manage.py test
```
Todos os 5 testes unitários de backend, rotas e APIs devem passar com `OK`.

---

## ❓ Resolução de Problemas Comuns

1. **Erro: `docker: command not found` ou erro ao conectar no daemon:**
   - Abra o aplicativo **Docker Desktop** no Windows e espere o ícone da baleia na barra de tarefas ficar estável (verde).
2. **Erro: `port is already allocated` (Porta 8000 já em uso):**
   - Pare o contêiner ou processo anterior rodando na porta 8000:
     ```bash
     docker stop cloudpulse_app
     docker rm cloudpulse_app
     ```
   - Ou rode mapeando para outra porta, por exemplo 8080:
     ```bash
     docker run -d -p 8080:8000 --name cloudpulse_app cloudpulse-backend:1.0
     ```
     E acesse via `http://localhost:8080`.
