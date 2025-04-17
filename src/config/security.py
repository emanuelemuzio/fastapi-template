from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from ..config import SessionDep, engine
from sqlmodel import select, Session
from ..model import UserEntity
from ..response import BaseError
from ..utils import from_env

SECRET_KEY = from_env('SECRET_KEY')
ALGORITHM = from_env('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(from_env('ACCESS_TOKEN_EXPIRE_MINUTES'))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def get_user(email : str, session : SessionDep) -> UserEntity | None:
    statement = select(UserEntity).where(UserEntity.email == email)
    user_entity = session.exec(statement=statement).one_or_none()
    return user_entity

def authenticate_user(email: str, password: str, session : SessionDep) -> UserEntity:
    user = get_user(email=email, session=session)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user    

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session : SessionDep) -> UserEntity:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(email=token_data.email, session=session)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserEntity, Depends(get_current_user)],
) -> UserEntity:
    if current_user.disabled:
        return BaseError(status=status.HTTP_400_BAD_REQUEST, message="Utente non attivo")
    return current_user

def check_default_user():
    with Session(engine) as session:
        statement = select(UserEntity).where(UserEntity.email == from_env('DEFAULT_EMAIL'))
        defaul_user_entity = session.exec(statement).first()

        if not defaul_user_entity:
            defaul_user_entity = UserEntity(
                email=from_env('DEFAULT_EMAIL'),
                name=from_env('DEFAULT_NAME'),
                password=get_password_hash(from_env('DEFAULT_PASSWORD'))
            )

            session.add(defaul_user_entity)
            session.commit()
            session.refresh(defaul_user_entity)