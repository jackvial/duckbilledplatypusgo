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

# Important to set this correctly so you don't run out of memory.
# When running a model server the model is loaded into memory for each worker.
# if your model is 500mb and you are running 6 workers then you will be using 3gb of ram.
# Set to 1 to begin with a keep an eye on your metrics to see if it needs to be increased
# and if you need to move to larger servers.
ENV MAX_WORKERS="1"
ENV WEB_CONCURRENCY="1"