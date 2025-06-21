from fastapi import APIRouter, FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi.responses import JSONResponse

import models
from models import User, FavoriteEvent
from schemas import UserCreate, Token, FavoriteEventCreate, FavoriteEventOut
from database import engine, get_db
from secretkey import getSECRETKEY
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


# Initialize app and DB
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or better, allow your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)

# Auth & crypto settings
SECRETKEY = getSECRETKEY()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
db_dependency = Annotated[Session, Depends(get_db)]

# Helper functions
def get_hashed_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRETKEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRETKEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except (jwt.PyJWTError, InvalidTokenError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user

# Routes
@app.post("/register")
def register_user(user: UserCreate, db: db_dependency):
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered user or username already taken"
        )

    hashed_password = get_hashed_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully", "user-id": new_user.id}

@app.post("/login", response_model=Token)
async def login_fn(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type="bearer")

# Favorites router
router = APIRouter()


@router.post("/mark_favorite", response_model=FavoriteEventOut)
async def mark_favorite(
    event: FavoriteEventCreate,
    db: db_dependency,
    current_user: User = Depends(get_current_user)
):
    try:
        favorite = FavoriteEvent(
            event_id=event.event_id,
            name=event.name,
            url=event.url,
            date=event.date,
            image_url=event.image_url,
            user_id=current_user.id
        )
        db.add(favorite)
        db.commit()
        db.refresh(favorite)

        return JSONResponse(content=jsonable_encoder(favorite))  # ✅ Return Pydantic model

    except Exception as e:
        print("❌ Error in /mark_favorite:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")




@router.get(
    "/favorites",
    response_model=list[FavoriteEventOut]  # or List[FavoriteEventOut] on <3.9
)
async def get_favorites(
    db: db_dependency,
    current_user: User = Depends(get_current_user)
):
    """
    Return all favourite events that belong to the current user.
    """
    favorites = (
        db.query(FavoriteEvent)
          .filter(FavoriteEvent.user_id == current_user.id)
          .order_by(FavoriteEvent.date)
          .all()
    )

    return [FavoriteEventOut.from_orm(fav) for fav in favorites]



app.include_router(router)
