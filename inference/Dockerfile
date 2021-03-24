# Inference Dockerfile
FROM tiangolo/uvicorn-gunicorn:python3.7

RUN apt-get install -y unzip curl; apt-get update -y;

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
    
# AWS Cli setup
# RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"; unzip awscliv2.zip; ./aws/install;

# ADD docker_config/aws /root/.aws

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./app/pyproject.toml ./app/poetry.lock* /app/

WORKDIR /app

RUN poetry install --no-root --no-dev

COPY ./app /app

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE