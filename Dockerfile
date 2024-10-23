# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY flappybot.py /app/flappybot.py

# Copy the local libs directory with wheel files into the container
COPY libs /app/libs

# Install the dependencies from the local libs directory
RUN pip install --no-index --find-links=/app/libs --no-cache-dir /app/libs/*.whl

# Run flappybot.py when the container launches
CMD ["python", "flappybot.py"]