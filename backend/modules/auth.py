from fastapi import APIRouter, Depends, HTTPException, Response, status

from security import (
    authenticate,
    clear_auth_cookie,
    create_access_token,
    get_current_user,
    set_auth_cookie,
)
from schemas import LoginRequest, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
def login(body: LoginRequest, response: Response):
    """Returns the JWT in the response body (as access_token) AND still sets
    it as an httpOnly cookie. The frontend uses the body token, sent as an
    Authorization: Bearer header on every request — this is what actually
    works when the frontend and backend are deployed on different
    *.onrender.com subdomains, since browsers (Incognito/private mode
    especially) block third-party cookies between them even though both
    are technically "onrender.com". The cookie is kept as a bonus for local
    dev, where the Vite proxy makes everything same-origin and the cookie
    alone is enough."""
    try:
        user = authenticate(body.email, body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    token = create_access_token(user)
    set_auth_cookie(response, token)
    return {**user, "access_token": token}


@router.post("/logout")
def logout(response: Response):
    clear_auth_cookie(response)
    return {"ok": True}


@router.get("/me", response_model=UserOut)
def me(user: dict = Depends(get_current_user)):
    return user
