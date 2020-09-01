import os
import re
import time
import logging
import random
from dotenv import load_dotenv

load_dotenv()

from typing import Optional, Dict
import secrets
from fastapi import Depends, FastAPI, HTTPException, status, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from stream_chat import StreamChat

logging.basicConfig(filename="requests.log", level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()
security = HTTPBasic()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://dev4.fuseclassroom.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex="https://.*\.fuseclassroom\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Start request path={request.url.path} Host={request.client.host}")

    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)

    logger.info(
        f"Completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    print(username, password)
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


class User(BaseModel):
    id: str
    name: str


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post("/v1/token")
async def create_token(user: User, username: str = Depends(get_current_username)):
    STREAM_API_KEY = os.getenv("STREAM_API_KEY")
    STREAM_API_SECRET = os.getenv("STREAM_API_SECRET")

    chat = StreamChat(api_key=STREAM_API_KEY, api_secret=STREAM_API_SECRET)

    data = {
        "id": user.id,
        "name": user.name,
        "role": "admin",
        "image": f"https://robohash.org/{user.id}",
    }

    token = chat.create_token(user.id)
    chat.update_user({"id": user.id, "name": user.name})

    logger.info(f"Token for user {user.id} created")

    return JSONResponse({"user": data, "token": token, "apiKey": STREAM_API_KEY})
