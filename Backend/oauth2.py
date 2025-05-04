from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List

from login_token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    creds_exception = HTTPException (
                            status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Access is not permitted",
                           headers={"WWW-Authenticate": "Bearer"}
                        )
    return await verify_token(token, creds_exception)



def allow_users(allowed_usernames: List[str]):
    def checker(user = Depends(get_current_user)):
        if user.email not in allowed_usernames:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return checker