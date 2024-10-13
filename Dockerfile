# Use an official Python runtime as a parent image
FROM python:3.9-slim

# install git
RUN apt-get update && apt-get install -y git

# Add group & user + sudo
RUN groupadd -r user && \
    useradd --create-home --gid user user && \
    mkdir -p /etc/sudoers.d && \
    echo 'user ALL=NOPASSWD: ALL' > /etc/sudoers.d/user

USER user
WORKDIR /home/user
ENV HOME=/home/user

# Set the working directory inside the container
WORKDIR /home/user/project

# Clone the repository
RUN git clone https://github.com/pprajap/tq_backend.git /home/user/project

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
