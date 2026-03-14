from jose import jwt, JWTError
import sys
<<<<<<< HEAD
from schemas.user_schema import UserCreate
=======

from schemas import UserCreate
>>>>>>> 86d3da5d9e1e4ea42f67bb7c99582b5d0b6695b0
sys.path.append("D:/auto_project")
from datetime import datetime, timedelta
import os
from sqlalchemy.orm import Session
from dependencies import get_db
from logger import logger
from dotenv import load_dotenv
from fastapi import APIRouter,Depends, HTTPException
<<<<<<< HEAD
from models.user import user
=======
from models import User
>>>>>>> 86d3da5d9e1e4ea42f67bb7c99582b5d0b6695b0
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password:str):
    return pwd_context.hash(password)
def verify_password(plain,hashed):
    return pwd_context.verify(plain, hashed)

load_dotenv()
<<<<<<< HEAD
print("ADMIN_SECRET_KEY:", os.getenv("ADMIN_SECRET_KEY"))
=======
>>>>>>> 86d3da5d9e1e4ea42f67bb7c99582b5d0b6695b0
router = APIRouter()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM =os.getenv("ALGORITHM")
ACCESS_TOKEN_TIME=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ADMIN_SECRET_KEY=os.getenv("ADMIN_SECRET_KEY")
def create_access_token(data:dict):
    to_encode = data.copy()
    expire =datetime.utcnow()+timedelta(minutes=int(ACCESS_TOKEN_TIME))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str=payload.get("sub")
        if username is None:
            raise HTTPException (status_code=401, detail="Unauthorized")
<<<<<<< HEAD
        User=db.query(user).filter(user.username == username).first()
        if not User:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return User
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.get("/me")
def get_me(current_user:user=Depends(get_current_user)):
    return current_user

@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm =Depends(),db:Session=Depends(get_db)):
    User=db.query(user).filter(user.username == form_data.username).first()
    
    if not User:
        logger.warning(f"Failed Login Attempt for {form_data.username}")
        return {"error":"Invalid username or password"}
    if not verify_password(form_data.password, User.hashed_password):
        logger.warning(f"Failed Login Attempt for {form_data.username}")
        return {"error":"Invalid password"}
    access_token = create_access_token(data={"sub": User.username})
=======
        user=db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm =Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.username == form_data.username).first()
    
    if not user:
        logger.warning(f"Failed Login Attempt for {form_data.username}")
        return {"error":"Invalid username or password"}
    if not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Failed Login Attempt for {form_data.username}")
        return {"error":"Invalid password"}
    access_token = create_access_token(data={"sub": user.username})
>>>>>>> 86d3da5d9e1e4ea42f67bb7c99582b5d0b6695b0
    logger.info(f"user login success for {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signin")
<<<<<<< HEAD
def signin(User:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(user).filter(user.username == User.username).first()
    if existing_user:
        logger.warning(f"user already exists for name {existing_user}")
        raise HTTPException(status_code=400, detail="username already exists")
    hased_password=hash_password(User.password)
    role="admin" if User.adminkey == ADMIN_SECRET_KEY else "user"
    new_user=user(username=User.username, hashed_password=hased_password, role=role)
    logger.info(f"signin success for user {User.username} with role {role}")
=======
def signin(user:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.warning(f"user already exists for name {existing_user}")
        raise HTTPException(status_code=400, detail="Username already exists")
    hased_password=hash_password(user.password)
    role="admin" if user.adminkey == ADMIN_SECRET_KEY else "user"
    new_user=User(username=user.username, hashed_password=hased_password, role=role)
    logger.info(f"signin success for user {user.username} with role {role}")
>>>>>>> 86d3da5d9e1e4ea42f67bb7c99582b5d0b6695b0
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
<<<<<<< HEAD
    return {"message":"user created successfully","user": new_user}
@router.get("/admin")
def get_admin(current_user:user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException (status_code=403, detail="Forbidden")
    return {"message":"welcome admin","user": current_user}
=======
    return {"message":"User created successfully","user": new_user}
@router.get("/admin")
def get_admin(current_user:User=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException (status_code=403, detail="Forbidden")
    return {"message":"welcome admin","user": current_user}
>>>>>>> 86d3da5d9e1e4ea42f67bb7c99582b5d0b6695b0
