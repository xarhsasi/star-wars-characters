import http
import logging

from fastapi import APIRouter, HTTPException

from src.depends import UserServiceDI
from src.users.constants import (
    CREATE_USERS_API_DESCRIPTION,
    USERS_AUTHENTICATION_API_DESCRIPTION,
)
from src.users.exceptions import UserAlreadyExistsError
from src.users.models import User
from src.users.schemas import UserAuth, UserCreate, UserResponse, UserWithCredentials
from src.utils.password import BCryptPasswordService

logger = logging.getLogger(__name__)

APP_NAME = "users"
users_router = APIRouter(prefix=f"/{APP_NAME}", tags=[APP_NAME])


@users_router.post("/auth", description=USERS_AUTHENTICATION_API_DESCRIPTION)
async def authenticate(
    UserServiceDI: UserServiceDI,
    user_auth: UserAuth,
) -> UserWithCredentials:
    if not user_auth:
        raise HTTPException(
            status_code=http.HTTPStatus.BAD_REQUEST,
            detail="Invalid credentials",
        )

    user = await UserServiceDI.authenticate(
        email=user_auth.email,
        password=user_auth.password,
        password_service=BCryptPasswordService(),
    )
    jwt_token = await UserServiceDI.token(user=user)
    return UserWithCredentials(
        id=user.id, full_name=user.full_name, email=user.email, token=jwt_token
    )


@users_router.post("/register", description=CREATE_USERS_API_DESCRIPTION)
async def create(
    UserServiceDI: UserServiceDI,
    user_create: UserCreate,
) -> UserResponse:
    user = User(
        full_name=user_create.full_name,
        email=user_create.email,
        password=user_create.password,
    )
    try:
        u = await UserServiceDI.create(obj=user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=http.HTTPStatus.BAD_REQUEST,
            detail=e.message,
        ) from e

    jwt_token = await UserServiceDI.token(user=u)
    return UserWithCredentials(
        id=user.id, full_name=user.full_name, email=user.email, token=jwt_token
    )
