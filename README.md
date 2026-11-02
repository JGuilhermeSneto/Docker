# 🐳 CloudPulse - Backend Django & Docker para Nuvem

Projeto desenvolvido para a disciplina de **Desenvolvimento Web para Nuvem**, demonstrando a criação de um backend em **Django**, frontend moderno com **Tailwind CSS**, conteinerização com **Docker** e fundamentação teórica completa exigida pelo professor.

---

## 📋 Sumário
1. [Visão Geral da Aplicação](#-visão-geral-da-aplicação)
2. [Fundamentação Teórica](#-fundamentação-teórica)
   - [O que são Contêineres](#1-o-que-são-contêineres)
   - [Imagens Docker e Camadas](#2-imagens-docker-e-camadas)
   - [O que é o Dockerfile](#3-o-que-é-o-dockerfile)
   - [Isolamento](#4-isolamento)
   - [Portabilidade](#5-portabilidade)
   - [Comparativo: Contêineres vs Máquinas Virtuais (VMs)](#6-comparativo-contêineres-vs-máquinas-virtuais-vms)
3. [Guia Prático: Como Rodar](#-guia-prático-como-rodar)
   - [Opção 1: Execução com Docker (Recomendada para o Trabalho)](#opção-1-execução-com-docker-recomendada)
   - [Opção 2: Execução com Docker Compose](#opção-2-execução-com-docker-compose)
   - [Opção 3: Execução Local sem Docker](#opção-3-execução-local-sem-docker)
4. [Roteiro de Apresentação para o Professor](#-roteiro-de-apresentação-para-o-professor)
5. [Endpoints da API REST](#-endpoints-da-api-rest)

---

## 🌟 Visão Geral da Aplicação

O **CloudPulse** é um painel de gerenciamento de tarefas e diagnóstico de nuvem que possui uma funcionalidade chave: **ele detecta e exibe dados do próprio ambiente onde está sendo executado**:
- **Hostname / Container ID:** Dentro do contêiner Docker, exibe o ID alfanumérico isolado gerado pelo Docker (ex: `7b9a4c8d1e2f`), provando ao vivo o isolamento do contêiner!
- **Sistema Operacional do Contêiner:** `Linux (Debian slim)` mesmo quando o host for Windows ou macOS.
- **Detecção de Ambiente:** Alerta visual animado indicando se está rodando em contêiner Docker isolado ou na máquina local.
- **CRUD Completo de Tarefas de Nuvem:** Criação, alteração de status e exclusão de tarefas categorizadas (Docker, Nuvem, DevOps, Backend).
- **Página de Teoria Integrada:** Acesse `/teoria/` na aplicação para ver o conteúdo acadêmico diretamente na interface gráfica.

---

## 📚 Fundamentação Teórica

### 1. O que são Contêineres?
Um **contêiner** é um pacote leve, autônomo e executável que inclui tudo o que é necessário para executar uma aplicação: código, runtime, ferramentas de sistema, bibliotecas e configurações.

Diferente da virtualização pesada, os contêineres funcionam utilizando recursos nativos do Kernel Linux:
- **Namespaces:** Provêem o **isolamento de visão**:
  - `PID`: Tabela de processos isolada (o processo da aplicação dentro do contêiner enxerga-se como PID 1).
  - `NET`: Interfaces de rede, portas e rotas IP próprias.
  - `MNT`: Ponto de montagem de sistema de arquivos próprio.
  - `UTS`: Hostname e nome de domínio independentes.
  - `IPC`: Comunicação entre processos isolada.
- **Control Groups (cgroups):** Provêem o **isolamento e medição de recursos de hardware**:
  - Limitadores de memória RAM máxima, percentual de núcleos de CPU e limites de I/O em disco.

### 2. Imagens Docker e Camadas
Uma **Imagem Docker** é um pacote imutável e somente-leitura (*read-only*) que funciona como o modelo (*blueprint*) para instanciar contêineres.

- **Camadas (Layers):** Cada linha de comando no `Dockerfile` (`FROM`, `RUN`, `COPY`) gera uma camada intermediária somente-leitura. O Docker utiliza um sistema de arquivos de união (*UnionFS / Overlay2*) para sobrepor essas camadas de forma transparente.
- **Cache de Build:** Camadas que não sofreram alterações são reaproveitadas do cache local, reduzindo drasticamente o tempo de recompilação.
- **Camada do Contêiner (Read-Write Layer):** Ao iniciar o contêiner, o Docker adiciona uma camada fina de leitura e escrita no topo das camadas estáticas. Quaisquer arquivos modificados são gravados apenas nessa camada efêmera (*Copy-on-Write*).

### 3. O que é o Dockerfile?
O `Dockerfile` é o arquivo de configuração declarativa que especifica a receita de bolo para a construção da imagem.

No nosso projeto, utilizamos:
```dockerfile
FROM python:3.11-slim       # Imagem base oficial enxuta Linux Debian
ENV PYTHONDONTWRITEBYTECODE=1 # Impede geração de lixo .pyc
ENV PYTHONUNBUFFERED=1      # Garante envio imediato de logs para o terminal
WORKDIR /app                # Diretório de trabalho dentro do contêiner
COPY requirements.txt /app/ # Copia apenas dependências primeiro (otimização de cache)
RUN pip install -r requirements.txt # Instala libs Python
COPY . /app/                # Copia o código-fonte
EXPOSE 8000                 # Documenta que a aplicação escuta na porta 8000
ENTRYPOINT ["/app/entrypoint.sh"] # Executa migrações do banco e seed antes do app
CMD ["gunicorn", "cloudproject.wsgi:application", "--bind", "0.0.0.0:8000"] # Servidor de produção
```

### 4. Isolamento
O contêiner não compartilha com o sistema hospedeiro:
- O sistema de arquivos (ele não pode acessar diretórios do seu computador a menos que um volume seja explicitamente montado via `-v`).
- As variáveis de ambiente locais.
- Os processos em execução (um `kill` no contêiner não atinge o hospedeiro).
- As portas de rede (a porta 8000 do contêiner só se torna acessível se você explicitamente fizer o encaminhamento com `-p 8000:8000`).

### 5. Portabilidade
A portabilidade garante o lema **"Build Once, Run Anywhere"** (Construa uma vez, execute em qualquer lugar). 
Como o contêiner carrega consigo a versão exata do Python, do Django, do Gunicorn e das bibliotecas C de base, o sistema funcionará exatamente da mesma forma:
- No computador do colega de grupo (Windows 11)
- No notebook do professor (macOS)
- No servidor de nuvem (AWS EC2, Google Cloud Run ou Azure AKS com Linux)

### 6. Comparativo: Contêineres vs Máquinas Virtuais (VMs)

| Característica | 🐳 Contêineres (Docker) | 🖥️ Máquinas Virtuais (VMs) |
| :--- | :--- | :--- |
| **Arquitetura** | Virtualização a nível de SO | Virtualização a nível de Hardware |
| **Camada de Mediação** | Docker Engine (compartilha Kernel do Host) | Hypervisor (Type 1 ou Type 2) |
| **Sistema Convidado** | Não requer SO Convidado (*Guest OS*) | Requer um SO Completo para cada VM |
| **Tempo de Inicialização**| **Milissegundos a poucos segundos** | Minutos (boot de BIOS e SO completo) |
| **Tamanho em Disco** | **Dezenas ou poucas centenas de MBs** | Vários Gigabytes (de 10 GB a 80 GB+) |
| **Consumo de Memória**| Mínimo (apenas o processo da aplicação) | Alto (memória dedicada reservada para o SO) |
| **Densidade** | Centenas de contêineres por máquina | Poucas dezenas de VMs por máquina |
| **Isolamento** | Lógico (Kernel Namespaces / cgroups) | Físico/Virtualizado (Hardware Hypervisor) |

---

## 🚀 Guia Prático: Como Rodar

### Pré-requisito
Certifique-se de que o **Docker Desktop** (no Windows ou Mac) ou o **Docker Engine** (no Linux) esteja instalado e iniciado.  
*(Caso ainda não tenha instalado no Windows, baixe em [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) e certifique-se de que a opção WSL2 esteja habilitada).*

---

### Opção 1: Execução com Docker (Recomendada)

Abra o terminal (PowerShell, CMD ou Bash) nesta pasta do projeto (`c:\Users\gu268\Projetos\docker`):

#### 1. Construir a Imagem Docker
```bash
docker build -t cloudpulse-backend:1.0 .
```
> O ponto (`.`) no final indica que o contexto de build é o diretório atual. O Docker executará todas as etapas do `Dockerfile`.

#### 2. Executar o Contêiner
```bash
docker run -d -p 8000:8000 --name cloudpulse_container cloudpulse-backend:1.0
```
- `-d`: Roda em segundo plano (*detached mode*).
- `-p 8000:8000`: Mapeia a porta 8000 do seu computador para a porta 8000 de dentro do contêiner.
- `--name cloudpulse_container`: Dá um nome amigável ao contêiner.

#### 3. Acessar a Aplicação no Navegador
- **Dashboard:** [http://localhost:8000](http://localhost:8000)
- **Página de Teoria Acadêmica:** [http://localhost:8000/teoria/](http://localhost:8000/teoria/)
- **API JSON de Diagnóstico:** [http://localhost:8000/api/system-info/](http://localhost:8000/api/system-info/)

#### 4. Comandos para o Professor Avaliar
```bash
# Listar o contêiner em execução e conferir portas e status
docker ps

# Ver os logs do Django e Gunicorn gerados dentro do contêiner
docker logs cloudpulse_container

# Entrar no terminal dentro do contêiner para provar o isolamento
docker exec -it cloudpulse_container bash

# Para parar e remover quando terminar a apresentação
docker stop cloudpulse_container
docker rm cloudpulse_container
```

---

### Opção 2: Execução com Docker Compose

Se preferir orquestrar com volume persistente para não perder dados ao reiniciar:

```bash
# Subir a aplicação
docker compose up --build -d

# Ver os logs
docker compose logs -f

# Parar a aplicação
docker compose down
```

---

### Opção 3: Execução Local sem Docker

Se quiser executar localmente com o ambiente virtual Python já configurado:

```powershell
# Ativar o ambiente virtual no Windows
.\.venv\Scripts\Activate.ps1

# Rodar as migrações (se necessário)
python manage.py migrate

# Iniciar o servidor de desenvolvimento
python manage.py runserver 8000
```
Acesse [http://127.0.0.1:8000](http://127.0.0.1:8000).  
*(Note que, ao rodar localmente, o banner superior indicará em laranja que a aplicação está executando no **Host Local**, e o Hostname será o nome do seu computador Windows).*

---

## 🎯 Roteiro de Apresentação para o Professor (5 minutos)

1. **Abertura:** Mostre o código do `Dockerfile` e do `docker-compose.yml`, explicando as diretivas (`FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`).
2. **Build da Imagem:** Execute `docker build -t cloudpulse-backend:1.0 .` no terminal e mostre as camadas sendo construídas ou recuperadas do cache.
3. **Execução:** Execute `docker run -d -p 8000:8000 --name cloudpulse_container cloudpulse-backend:1.0`.
4. **Demonstração do Isolamento:**
   - Abra [http://localhost:8000](http://localhost:8000).
   - Aponte para o banner: o **Hostname exibido é o Container ID gerado pelo Docker** (ex: `8f3b12a0d9e4`) e o sistema operacional é **Linux Debian**, provando que o backend está totalmente isolado do Windows hospedeiro.
5. **Demonstração Prática:**
   - Crie uma nova tarefa pelo botão "+ Nova Tarefa" e altere seu status.
   - Clique em **"Testar API JSON"** para mostrar a resposta do backend Django em tempo real.
6. **Teoria Integrada:**
   - Clique na aba **"📘 Teoria Docker & VMs"** ou acesse `/teoria/` e explique o quadro comparativo de Contêineres vs VMs e os conceitos de Namespaces e cgroups.

---

## 📡 Endpoints da API REST

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Dashboard principal com métricas e gestão de tarefas |
| `GET` | `/teoria/` | Documentação teórica sobre Docker e VMs |
| `GET` | `/api/system-info/` | Telemetria do contêiner e dados de isolamento em JSON |
| `GET` | `/api/tasks/` | Lista todas as tarefas em JSON |
| `POST` | `/tasks/create/` | Criação de uma nova tarefa |
| `POST` | `/tasks/<id>/status/` | Atualização do status da tarefa |
| `POST` | `/tasks/<id>/delete/` | Exclusão de tarefa |

