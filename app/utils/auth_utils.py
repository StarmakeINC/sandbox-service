from typing import Dict, Any
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from app.config import settings
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional


class AuthUtils:
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    pwd_context = CryptContext(schemes=["django_pbkdf2_sha256"], deprecated="auto")

    @classmethod
    def verify_and_refresh_token(cls, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload