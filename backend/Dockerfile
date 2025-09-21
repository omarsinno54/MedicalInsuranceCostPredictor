# Dockerfile for Flask backend
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .
COPY Makefile .

# Make sure `make` is installed in your base image
RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists*

# Install dependencies
RUN make install

# Copy app files
COPY app.py .
COPY *.pkl .

# Expose port
EXPOSE 5010

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run app
CMD ["make", "app"]