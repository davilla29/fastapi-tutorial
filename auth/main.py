from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from auth_database import get_db, Base, engine
from jose import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(access_token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try: 
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credential_exception
        
    except JWTError:
        raise credential_exception
    
    return {"username": username, "role": role}

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}! You have accessed a protected route.", "role": current_user['role']}

def require_roles(allowed_roles: list):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")
        return current_user
    return role_checker

@app.get("/profile")
def profile(current_user: dict = Depends(require_roles(["user", "admin"]))):
    return {"message": f"Hello, {current_user['username']}! This is your profile.", "role": current_user['role']}

@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(require_roles(["user"]))):
    return {"message": f"Welcome to the user dashboard"}


@app.get("/admin/dashboard")
def admin_dashboard(current_user: dict = Depends(require_roles(["admin"]))):
    return {"message": f"Welcome to the admin dashboard"}