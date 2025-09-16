import http
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.utils.jwt import (
    JwtAuthenticationService,
    JwtHTTPBearer,
)
from src.utils.password import BCryptPasswordService
from src.depends import get_db
from src.users.constants import (
    LIST_USERS_API_DESCRIPTION,
    USERS_AUTHENTICATION_API_DESCRIPTION,
)
from src.users.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.users.schemas import (
    UserAuth,
    UserResponse,
    UserWithCredentials,
)
from src.users.repository import UserRepository

logger = logging.getLogger(__name__)

APP_NAME = "users"
user_router = APIRouter(prefix=f"/{APP_NAME}", tags=[APP_NAME])


@user_router.post("/auth", description=USERS_AUTHENTICATION_API_DESCRIPTION)
async def authenticate(
    user_auth: UserAuth,
    db: Session = Depends(get_db),
) -> UserWithCredentials:
    if not user_auth:
        raise HTTPException(
            status_code=http.HTTPStatus.BAD_REQUEST,
            detail="Invalid credentials",
        )
    user = await UserRepository(session=db).authenticate_user(
        username=user_auth.email,
        password=user_auth.password,
        password_service=BCryptPasswordService(),
    )
    jwt_token = JwtAuthenticationService().encode(user_id=user.id)
    return UserWithCredentials(
        id=user.id, full_name=user.full_name, email=user.email, token=jwt_token
    )


@user_router.get(
    "/",
    description=LIST_USERS_API_DESCRIPTION,
    dependencies=[Depends(JwtHTTPBearer())],
)
async def list_users(
    db: Session = Depends(get_db),
) -> list[UserResponse]:
    user_service = UserRepository(session=db)
    users = list(await user_service.users())
    return users