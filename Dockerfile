# Use an official Python runtime as the base image.
FROM python:3.11-slim

# Set environment variables for Python: ensure stdout and stderr are flushed.
ENV PYTHONUNBUFFERED=1

# Set the working directory.
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Copy the Alembic configuration file and the migrations directory.
# COPY alembic.ini .
# COPY alembic/ alembic/

# # Run Alembic migrations.
# RUN alembic upgrade head

# Expose the port that FastAPI will run on.
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

