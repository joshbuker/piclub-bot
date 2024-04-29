FROM python:3.10

WORKDIR /bot

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

# Copy all python files into /bot/app/
COPY ./app/ ./app

ENTRYPOINT ["python", "./app/main.py"]
