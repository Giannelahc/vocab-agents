

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_auth_service
from schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter()

@router.post("/register")
async def register(
    request: RegisterRequest,
    auth_service = Depends(get_auth_service)
):

    try:

        await auth_service.register(
            request.name,
            request.lastname,
            request.username,
            request.email,
            request.password
        )

        return {
            "message": "User created"
        }

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
    
@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, auth_service = Depends(get_auth_service)):

    try:

        token = await auth_service.login(
            request.email,
            request.password
        )
        return TokenResponse(
            access_token=token,
            token_type="Bearer"
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=401,
            detail=str(ex)
        )