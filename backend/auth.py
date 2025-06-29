from datetime import datetime , timedelta , timezone
import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from secretkey import getSECRETKEY

SECRETKEY = getSECRETKEY()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes = ["bcrypt"] , deprecated = "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password , hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)

def create_access_token(data : dict , expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode , SECRETKEY , algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token : dict):
    try:
        payload = jwt.decode(token , SECRETKEY , algorithms = [ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

