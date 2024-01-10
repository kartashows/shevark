FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv python3-dev

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Create a virtual environment
RUN python3 -m venv /venv

# Set the PATH to include the virtual environment
ENV PATH="/venv/bin:$PATH"

# Install Python dependencies
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy bot files into the container
COPY . /app

CMD ["python3", "bot_script.py", "--postgres-host=postgres"]
