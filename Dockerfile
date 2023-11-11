# Use an official PostgreSQL image as the base image
FROM postgres:latest

COPY init.sql /docker-entrypoint-initdb.d/

# Install Python and necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your bot files into the container
COPY . /app

# Start your bot here (replace 'bot_script.py' with your actual bot script name)
CMD ["python3", "bot_script.py"]