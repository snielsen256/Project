# Use the official Python 3.11 slim image from the Docker Hub
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Command to run your Python script
CMD ["python", "app.py"]