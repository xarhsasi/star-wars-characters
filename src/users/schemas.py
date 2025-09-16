from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    model_config = {
        "from_attributes": True  # Allows parsing from ORM attributes in Pydantic v2
    }


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserWithCredentials(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    token: str


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
