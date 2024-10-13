# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# install git
RUN apt-get update && apt-get install -y git

# Clone the repository
RUN git clone https://github.com/pprajap/tq_backend.git /app

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]

# build the Docker image
# docker build -t tq_backend .

# run the Docker container
# docker run -it --rm -p 5000:5000 tq_backend
