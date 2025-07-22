from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username : str
    email : EmailStr

class UserCreate(UserBase):
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class UserResponse(UserBase):
    id : str

class TokenResponse(BaseModel):
    user : UserResponse
    token : str