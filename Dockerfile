# official PostgreSQL image as the base image
FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/

RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

RUN python3 -m venv /venv

ENV PATH="/venv/bin:$PATH"

RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy bot files into the container
COPY . /app

CMD ["python3", "bot_script.py"]
