from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db, Base, engine
from jose import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Helper function that takes user data
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user exists or not
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password 
    hashed_pass = utils.hash_password(user.password)

    #create a new user
    new_user = models.User(username = user.username, email=user.email, hashed_password=hashed_pass, role=user.role)

    # Save the user to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Return the value excluding password
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "role": new_user.role, "message": "User created successfully"}


@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token_data = {"sub": user.username, 'role': user.role}

    # Create an access token
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}