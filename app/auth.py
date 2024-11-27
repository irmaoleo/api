from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

from .database import users_collections
from .schemas.users import individual_serial
from .services.password import password_generator
from .services.emails import send_email


router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreatedUserRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    acess_token: str
    token_type: str
    
class ResetPasswordRequest(BaseModel):
    email: str

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreatedUserRequest):

    user_with_email = users_collections.find_one({"email": user.email})

    if user_with_email != None:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    else:

        hashed_password = bcrypt_context.hash(user.password)
        user_dict = {
            "email": user.email, 
            "password": hashed_password, 
            "fullName": "", 
            "birthDate": "", 
            "postalCode": "", 
            "gender": ""
            }
    

        users_collections.insert_one(user_dict)

        return {"email": user.email, "message": "User created successfully"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(userLogin: CreatedUserRequest):

    user = users_collections.find_one({"email": userLogin.email})

    if user is not None:

        founded_user = individual_serial(user)

        if bcrypt_context.verify(userLogin.password, founded_user["password"]):




            access_token = jwt.encode(
                {"sub": founded_user["_id"]},
                SECRET_KEY,
                algorithm=ALGORITHM,
            )  
            

            return {"access_token": access_token, "token_type": "bearer"}  # or JWT

        else:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
            )

    else:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

@router.post('/reset', status_code=status.HTTP_200_OK)
async def reset_password(user: ResetPasswordRequest):
    user_with_email = users_collections.find_one({"email": user.email})

    if user_with_email is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        
        # criar nova senha
       
        new_password = password_generator()
        hashed_password = bcrypt_context.hash(new_password)  
        users_collections.update_one({"email": user.email}, {"$set": {"password": hashed_password}})
        # enviar para o usuario
        
        send_email({
            "email": user.email,
            "password": new_password,
            "full_name": ""  # or user_with_email["fullName"]
            }, "nova senha")
        
        

        return {"message": "Password reset successfully"}
    

def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return payload["sub"]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )
