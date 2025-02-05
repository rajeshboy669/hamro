# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on (Render or any cloud platform uses this to bind)
EXPOSE 5000

# Run gunicorn to serve the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "server:app"]
