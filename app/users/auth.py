from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from app.config import get_auth_data

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash_password: str) -> bool:
    return pwd_context.verify(password, hash_password)


def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expire_date = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({'exp': expire_date})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], auth_data['algorithm'])
    return encode_jwt
