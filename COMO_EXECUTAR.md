# 🚀 Guia de Execução & Roteiro do Seminário — CloudPulse

Este documento contém o passo a passo completo e à prova de falhas para executar o projeto no seu computador, na máquina de um colega ou na máquina do professor durante o seminário de **Desenvolvimento Web para Nuvem com Docker**.

---

## 🔗 Repositório Oficial do Projeto no GitHub

* **Repositório Git:** [https://github.com/JGuilhermeSneto/Docker.git](https://github.com/JGuilhermeSneto/Docker.git)
* **Branch Principal:** `main`
* **Nome da Imagem Docker:** `cloudpulse-backend:1.0`
* **Nome do Contêiner:** `cloudpulse_app`

### 📥 Como clonar o projeto em uma nova máquina (se necessário):
```bash
git clone https://github.com/JGuilhermeSneto/Docker.git
cd Docker
```
*(Caso já esteja no seu computador atual, basta abrir o terminal e entrar em: `cd C:\Users\gu268\Projetos\docker`)*.

---

## ⚠️ Pré-requisitos Obrigatórios antes de Começar

1. **Docker Desktop Aberto:**
   - Abra o **Docker Desktop** no Windows e certifique-se de que a luzinha no canto inferior esquerdo está **verde** (🟢 *Engine running*).
2. **WSL 2 Ativo (Apenas se estiver em outra máquina Windows nova):**
   - Caso use outra máquina Windows que nunca rodou Docker antes, abra o PowerShell como Administrador e execute:
     ```powershell
     wsl --install --no-distribution
     ```
     *(E reinicie o computador se solicitado).*

---

## ⚡ Passo a Passo de Execução com Docker (Oficial para o Seminário)

Abra o terminal (PowerShell, CMD ou Bash) **dentro da pasta do projeto**:

### 1️⃣ Construir a Imagem Docker (`docker build`)
```bash
docker build -t cloudpulse-backend:1.0 .
```
> 💡 **Atenção:** Repare no espaço e no ponto **`.`** no final do comando. Ele indica que o Docker deve usar o `Dockerfile` do diretório atual.

---

### 2️⃣ Executar o Contêiner (`docker run`)
```bash
docker run -d -p 8000:8000 --name cloudpulse_app cloudpulse-backend:1.0
```
* **O que cada parâmetro faz (bom explicar ao professor):**
  * `-d` (*detached*): Executa o contêiner em segundo plano, liberando o terminal.
  * `-p 8000:8000`: Mapeia a porta 8000 do Windows (host) para a porta 8000 de dentro do contêiner.
  * `--name cloudpulse_app`: Dá um nome fácil de referenciar para o contêiner.
  * `cloudpulse-backend:1.0`: É a imagem que construímos no passo 1.

---

### 3️⃣ Acessar a Aplicação no Navegador
* 🌐 **Painel de Controle & Aplicação:** [http://localhost:8000](http://localhost:8000)
* 📘 **Página de Teoria Embutida:** [http://localhost:8000/teoria/](http://localhost:8000/teoria/)
* 📡 **API JSON de Diagnóstico:** [http://localhost:8000/api/system-info/](http://localhost:8000/api/system-info/)

---

## 🎤 Roteiro de Demonstração para o Seminário (Script de 5 Minutos)

Durante a apresentação para o professor, siga este roteiro prático para tirar nota máxima:

### 1. Mostrar o Contêiner Ativo no Terminal
```bash
docker ps
```
> **Explicação:** Mostre que o contêiner `cloudpulse_app` está com status `Up`, rodando a imagem `cloudpulse-backend:1.0` e encaminhando a porta `0.0.0.0:8000->8000/tcp`.

### 2. Mostrar os Logs da Aplicação
```bash
docker logs --tail 20 cloudpulse_app
```
> **Explicação:** Mostre que o script de entrada (`entrypoint.sh`) aplicou as migrações do banco SQLite, populou os dados iniciais e iniciou o servidor WSGI Gunicorn com múltiplos workers.

### 3. Provar o Isolamento de Sistema Operacional (O Ponto Alto da Apresentação!)
No terminal, execute:
```bash
docker exec -it cloudpulse_app bash
```
Agora você está **dentro do contêiner Linux**! Execute estes 2 comandos:
```bash
# 1. Mostrar o hostname isolado (será exatamente o ID alfanumérico do contêiner):
hostname

# 2. Mostrar que é um sistema Linux rodando mesmo dentro do Windows:
uname -a
```
Para sair do contêiner e voltar ao Windows, basta digitar:
```bash
exit
```

### 4. Apresentar a Interface Web
Abra [http://localhost:8000](http://localhost:8000) no projetor/navegador e aponte para:
1. **Banner Superior:** Mostra em tempo real que o Hostname coincide com o Container ID e o SO é Linux Debian.
2. **CRUD Funcional:** Crie uma tarefa de teste (ex: *"Apresentação do Seminário de Nuvem"*).
3. **Botão "Testar API JSON":** Clique para demonstrar a resposta da API REST em formato JSON com métricas de telemetria.
4. **Aba "📘 Teoria Docker & VMs":** Clique no menu superior para exibir os slides conceituais e o comparativo completo de **Contêineres vs Máquinas Virtuais (VMs)**.

---

## 📦 Método Alternativo: Execução com Docker Compose

Se preferir usar o `docker compose` (com volume persistente configurado):

```bash
# Iniciar a aplicação
docker compose up --build -d

# Visualizar logs em tempo real
docker compose logs -f

# Parar a aplicação
docker compose down
```

---

## 🛑 Gerenciamento do Contêiner (Comandos Úteis)

* **Parar o contêiner:**
  ```bash
  docker stop cloudpulse_app
  ```
* **Iniciar o contêiner novamente (sem precisar rebuildar):**
  ```bash
  docker start cloudpulse_app
  ```
* **Remover o contêiner (para recriar do zero):**
  ```bash
  docker rm -f cloudpulse_app
  ```
* **Ver consumo de CPU e Memória RAM em tempo real:**
  ```bash
  docker stats cloudpulse_app
  ```

---

## ❓ Resolução de Problemas no Dia da Apresentação

1. **Erro: `failed to connect to the docker API`:**
   - O Docker Desktop está fechado. Abra o **Docker Desktop** no Menu Iniciar e espere a luzinha verde 🟢 acender.
2. **Erro: `port is already allocated` (Porta 8000 ocupada):**
   - Já existe um contêiner rodando. Remova-o com:
     ```bash
     docker rm -f cloudpulse_app
     ```
   - E execute o comando `docker run` novamente.
3. **Erro: `docker: 'docker buildx build' requires 1 argument`:**
   - Você esqueceu de colocar o ponto final `.` no final do comando `docker build -t cloudpulse-backend:1.0 .`.
