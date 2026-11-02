# =======================================================
# Dockerfile para Aplicação Backend Django em Nuvem
# =======================================================

# 1. Imagem Base Oficial Python (versão slim baseada em Debian Linux)
FROM python:3.11-slim

# Metadados informativos
LABEL maintainer="Grupo de Desenvolvimento Web para Nuvem"
LABEL description="Backend Django containerizado com Docker"

# 2. Variáveis de ambiente para otimização do Python em contêineres
# Evita a gravação de arquivos .pyc no disco do contêiner
ENV PYTHONDONTWRITEBYTECODE=1
# Envia logs diretamente para o stdout/stderr sem buffering
ENV PYTHONUNBUFFERED=1
# Identificador de ambiente em nuvem/contêiner
ENV IN_DOCKER=true
ENV APP_ENV="Docker Cloud Production"

# 3. Diretório de trabalho dentro do contêiner
WORKDIR /app

# 4. Instala dependências do sistema operacional
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Otimização de Camadas (Cache do Docker):
# Copia primeiro apenas o requirements.txt para aproveitar o cache de camadas
COPY requirements.txt /app/

# 6. Instalação das dependências Python sem cache para reduzir imagem
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copia todo o código-fonte da aplicação para o contêiner
COPY . /app/

# Corrige quebras de linha Windows CRLF para LF e dá permissão de execução
RUN sed -i 's/\r$//' /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# 8. Coleta arquivos estáticos para o WhiteNoise servir em produção
RUN python manage.py collectstatic --noinput

# 9. Documenta a porta HTTP do contêiner
EXPOSE 8000

# 10. Script de entrada (executa migrações antes de subir o servidor)
ENTRYPOINT ["/app/entrypoint.sh"]

# 11. Comando padrão com servidor de produção WSGI Gunicorn
CMD ["gunicorn", "cloudproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]

