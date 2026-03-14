from fastapi import FastAPI
from database import engine
from database import Base
from dotenv import load_dotenv
from routes import auth,users
from models.user import user

load_dotenv()

app = FastAPI()
app.include_router(auth.router,prefix="/auth",tags=["auth"])
app.include_router(users.router,prefix="/users",tags=["users"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message":"welcome to the authentication system"}