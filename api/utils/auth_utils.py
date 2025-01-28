from fastapi.encoders import jsonable_encoder
import jwt

from config import JWT_SECRET


def create_jwt_token(content):
    encoded = jwt.encode(jsonable_encoder(content), JWT_SECRET, algorithm="HS256")
    return encoded


def decode_jwt_token(jwt_token):
    return jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
