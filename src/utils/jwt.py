import datetime
import jwt
import http
from fastapi.security import OAuth2PasswordBearer
from src.settings import Settings
from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.AUTH_CONFIG.JWT_TOKEN_URL)

class JwtAuthenticationService:
    """Service to encode and decode JWT tokens."""
    def __init__(self, settings: Settings = Settings()):
        self.secret_key = settings.AUTH_CONFIG.JWT_SECRET_KEY
        self.algorithm = settings.AUTH_CONFIG.JWT_ALGORITHM
        self.access_token_expire_minutes = settings.AUTH_CONFIG.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    def encode(self, user_id: int) -> str:
        """Encode a payload into a JWT token."""
        expire = datetime.datetime.now() + datetime.timedelta(minutes=self.access_token_expire_minutes)
        payload = {"sub": str(user_id),
                   "expire": expire.strftime("%Y-%m-%d %H:%M:%S")
                }
        return jwt.encode(payload, key=self.secret_key, algorithm=self.algorithm)

    def verify(self, token: HTTPAuthorizationCredentials) -> dict:
        """Decode a JWT token into a payload or raise an exception if not possible."""
        # This might raise an exception if token is invalid.
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        


class JwtHTTPBearer(HTTPBearer):
     def __init__(self, auth_service: JwtAuthenticationService = JwtAuthenticationService()):
        self.auth_service = auth_service
        super().__init__(auto_error=True)

     async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="Invalid authentication scheme.")
            if not self.auth_service.verify(credentials.credentials):
                raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="Invalid authorization code.")