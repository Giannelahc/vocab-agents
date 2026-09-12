

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from dependencies import get_auth_service, oauth2_scheme
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter()


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/register")
async def register(
    request: RegisterRequest,
    auth_service = Depends(get_auth_service)
):

    try:

        user = await auth_service.register(
            request.name,
            request.lastname,
            request.username,
            request.email,
            request.password
        )

        return {
            "id": user.id,
            "email": user.email
        }

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
    
@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, auth_service = Depends(get_auth_service)):

    try:

        token_payload = await auth_service.login(
            request.email,
            request.password
        )
        return TokenResponse(
            access_token=token_payload["access_token"],
            refresh_token=token_payload["refresh_token"],
            token_type=token_payload["token_type"]
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=401,
            detail=str(ex)
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshTokenRequest, auth_service = Depends(get_auth_service)):
    try:
        access_token = await auth_service.refresh(request.refresh_token)
        return TokenResponse(
            access_token=access_token,
            refresh_token=request.refresh_token,
            token_type="Bearer"
        )
    except Exception as ex:
        raise HTTPException(status_code=401, detail=str(ex))


@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    auth_service = Depends(get_auth_service),
):
    try:
        await auth_service.logout(token)
        return {"message": "Logged out successfully"}
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))