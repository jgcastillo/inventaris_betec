from fastapi import APIRouter, Depends
from modules.users.auths.auth_dependencies import GetCurrentActiveUser
from modules.users.permissions.permissions_services import PermissionsService
from modules.users.users.user_schemas import UserInDB
from shared.utils.service_result import ServiceResult, handle_result

router = APIRouter(
    prefix="/permissions",
    # tags=["permissions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list", name="permissions:list-permissions")
async def list_permissions(
    current_user: UserInDB = Depends(
        GetCurrentActiveUser(permission="permissions:list-permissions")
    ),
):
    result = await PermissionsService().list_permissions()
    return handle_result(result)
