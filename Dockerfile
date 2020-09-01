FROM python:3.8-slim-buster

# Set the working directory.
WORKDIR /app

# Copy the file from your host to your current location.
COPY . .

RUN pip install -r requirements.txt

EXPOSE 10001 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","10001"]
