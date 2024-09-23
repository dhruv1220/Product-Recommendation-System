# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.11-slim

# Set environment variables to ensure Python behaves properly in Docker
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1  
# Ensures output is immediately logged
ENV PYTHONUNBUFFERED=1  

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Expose the port your app runs on
EXPOSE 5001

# Command to run the application using Gunicorn
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5001", "app:app"]