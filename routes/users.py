from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from models.user import user
from routes.auth import get_current_user
from backend.logger import logger
router = APIRouter()
@router.get("/")
def get_users(current_user:user=Depends(get_current_user),db:Session=Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    users = db.query(user).all()
    return users

@router.delete("/{username}")
def delete_user(username:str,current_user:user=Depends(get_current_user),db:Session=Depends(get_db)):
    if not current_user:
        logger.warning(f"unauthorized user trying to delete user {username}")
        raise HTTPException(status_code=401, detail="Unauthorized")
    if current_user.role != "admin":
        logger.warning(f"user trying to delete with out access of admin")
        raise HTTPException(status_code=403, detail="Only admin can delete users")
    if username == current_user.username:
        logger.warning(f"user/admin {username} trying to delete himself")
        raise HTTPException(status_code=400, detail="Admin cannot delete themselves")

    User=db.query(user).filter(user.username == username).first()
    if not User:
        logger.warning(f"someone tried to delete non existing user")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"delete of user {username} successfull by {current_user.username}")
    db.delete(User)
    db.commit()
    return {"message": f"User {username} deleted successfully"}

@router.get("/profile")
def get_profile(current_user:user=Depends(get_current_user),db:Session=Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message" : "protected route access","user": current_user}