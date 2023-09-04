# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Clone your GitHub repository
RUN apt-get update \
    && apt-get install -y git \
    && git clone https://github.com/Aureliolo/discord-bot.git .

# Install any needed packages specified in requirements.txt
RUN pip install discord.py

# Run the script when the container launches
CMD ["python", "./discord_bot.py"]
