from typing import Dict
from uuid import UUID

from databases import Database
from fastapi import APIRouter, Body, Depends, Path, status
from loguru import logger
from modules.users.auths.auth_dependencies import GetCurrentActiveUser
from modules.users.auths.auth_exceptions import AuthExceptions
from modules.users.auths.auth_utils import is_authorized
from modules.users.roles.role_schemas import (
    RoleCreate,
    RoleIn,
    RoleOut,
    RoleUpdate,
    RoleUpdateActive,
)
from modules.users.roles.role_services import RoleService
from modules.users.users.user_schemas import UserInDB
from shared.core.db.db_dependencies import get_database
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter(
    prefix="/roles",
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=RoleOut,
    name="roles:create-role",
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    role: RoleCreate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(GetCurrentActiveUser("roles:create-role")),
) -> ServiceResult:
    new_role = RoleIn(**role.dict())
    new_role.created_by = current_user.id
    new_role.updated_by = current_user.id
    result = await RoleService(db).create_role(new_role)
    return handle_result(result)


@router.get(
    "/", response_model=Dict, name="roles:roles_list", status_code=status.HTTP_200_OK
)
async def get_roles_list(
    search: str | None = None,
    page_number: int = 1,
    page_size: int = 10,
    order: str = "",
    direction: str = "",
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(GetCurrentActiveUser("roles:roles_list")),
) -> ServiceResult:
    result = await RoleService(db).get_roles_list(
        search=search,
        page_num=page_number,
        page_size=page_size,
        order=order,
        direction=direction,
    )
    return handle_result(result)


@router.get("/{id}/", response_model=RoleOut, name="roles:get-role-by-id")
async def get_role_by_id(
    id: UUID,
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(GetCurrentActiveUser("roles:get-role-by-id")),
) -> ServiceResult:
    result = await RoleService(db).get_role_by_id(id=id)
    return handle_result(result)


@router.put("/{id}", response_model=RoleOut, name="roles:update-role-by-id")
async def update_role_by_id(
    id: UUID = Path(..., title="The id of the role to update"),
    role_update: RoleUpdate = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(GetCurrentActiveUser("roles:update-role-by-id")),
) -> ServiceResult:
    result = await RoleService(db).update_role(
        id=id, role_update=role_update, current_user_id=current_user.id
    )
    return handle_result(result)


@router.put(
    "/activate/{id}", response_model=RoleOut, name="roles:update-activate-role-by-id"
)
async def update_activate_role_by_id(
    id: UUID = Path(..., title="The id of the role to update is_active"),
    role_update: RoleUpdateActive = Body(..., embed=True),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(
        GetCurrentActiveUser("roles:update-activate-role-by-id")
    ),
) -> ServiceResult:
    result = await RoleService(db).update_activate_role(
        id=id, role_update=role_update, current_user_id=current_user.id
    )
    return handle_result(result)


@router.delete("/{id}", response_model=UUID, name="roles:delete-role-by-id")
async def delete_role_by_id(
    id: UUID = Path(..., title="The id of the role to update is_active"),
    db: Database = Depends(get_database),
    current_user: UserInDB = Depends(GetCurrentActiveUser("roles:delete-role-by-id")),
) -> ServiceResult:
    result = await RoleService(db).delete_role(id=id, current_user=current_user)
    return handle_result(result)
