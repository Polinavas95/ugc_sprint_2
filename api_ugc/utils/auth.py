from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from config.config import get_settings

oauth_schema = HTTPBearer()
settings = get_settings()


async def auth(
    authorization: HTTPAuthorizationCredentials = Security(oauth_schema),
) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(
            authorization.credentials,
            settings.app_settings.secret_key,
            algorithms=[settings.app_settings.algorithm],
        )
        user_id: str = payload.get('sub')
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
