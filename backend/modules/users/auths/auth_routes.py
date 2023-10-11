from typing import Dict, List
from uuid import UUID

from databases import Database
from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from icecream import ic
from loguru import logger
from modules.users.auths.auth_schemas import (
    AuthEmailRecoverPsw,
    AuthResetPsw,
    AuthResponse,
)
from modules.users.auths.auth_services import AuthService
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=AuthResponse, name="auth:login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    db: Database = Depends(get_database),
) -> ServiceResult:
    result = await AuthService().authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )

    return handle_result(result)


@router.post(
    "/forgot_password",
    response_model=Dict,
    name="auth:forgot_password",
    status_code=status.HTTP_200_OK,
)
async def forgotten_psw(
    email: AuthEmailRecoverPsw = Body(..., embed=True),
    db: Database = Depends(get_database),
) -> ServiceResult:
    result = await AuthService().forgot_psw(
        db=db, email=str(email.email).strip().lower()
    )

    return handle_result(result)


@router.get(
    "/verify_token",
    response_model=Dict,
    name="auth:verify_token",
    status_code=status.HTTP_200_OK,
)
async def verify_token(
    token: str,
    db: Database = Depends(get_database),
) -> ServiceResult:
    result = await AuthService().verify_token(token=token, db=db)

    return handle_result(result)


@router.post(
    "/reset_password",
    response_model=Dict,
    name="auth:reset_password",
    status_code=status.HTTP_200_OK,
)
async def reset_psw(
    token: str,
    new_psw: AuthResetPsw = Body(..., embed=True),
    db: Database = Depends(get_database),
) -> ServiceResult:
    result = await AuthService().reset_password(token=token, new_psw=new_psw, db=db)

    return handle_result(result)
