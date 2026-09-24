from fastapi import APIRouter, Depends, HTTPException, Response, status

from schemas import LoginRequest, UserOut
from security import (
    authenticate,
    clear_auth_cookie,
    create_access_token,
    get_current_user,
    set_auth_cookie,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=UserOut)
def login(body: LoginRequest, response: Response):
    try:
        user = authenticate(body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    token = create_access_token(user)
    set_auth_cookie(response, token)
    return user


@router.post("/logout")
def logout(response: Response):
    clear_auth_cookie(response)
    return {"ok": True}


@router.get("/me", response_model=UserOut)
def me(user: dict = Depends(get_current_user)):
    return user
