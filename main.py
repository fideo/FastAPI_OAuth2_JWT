from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi.exceptions import HTTPException
from jose import jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users = {
    "fideo": {"username": "fideo",
              "email": "federicomazzei@gmail.com",
              "password": "12345"},
    "lore": {"username": "lore",
             "email": "lorenamiele@gmail.com",
             "password": "12345"}
}


def encode_token(payload: dict) -> str:
    # Poner en una variable de entorno my-secret
    token = jwt.encode(payload, "my-secret", algorithm="HS256")
    return token


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    data = jwt.decode(token, "my-secret", algorithms=["HS256"])
    user = users.get(data["username"])
    return user


@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        raise HTTPException(
            status_code=400,
            detail="Incorrect Username or Password"
        )
    token = encode_token({"username": user["username"],
                          "email": user["email"]})
    return {"access_token": token}


@app.get("/users/profiles")
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user
