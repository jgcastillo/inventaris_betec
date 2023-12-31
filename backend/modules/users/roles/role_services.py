from typing import List
from uuid import UUID

from databases import Database
from loguru import logger
from modules.users.permissions import verify_permissions
from modules.users.roles.role_exceptions import RoleExceptions
from modules.users.roles.role_repositories import RoleRepository
from modules.users.roles.role_schemas import RoleIn, RoleUpdate, RoleUpdateActive
from modules.users.users.user_repositories import UserRepository
from modules.users.users.user_schemas import UserInDB
from shared.core import config
from shared.core.db.db_session_mixing import AppService
from shared.utils.service_result import ServiceResult
from shared.utils.short_pagination import short_pagination
from shared.utils.verify_uuid import is_valid_uuid


class RoleService(AppService):
    async def create_role(self, role: RoleIn) -> ServiceResult:
        if not role.role:
            logger.error("Try to create a rol with no name")
            return ServiceResult(RoleExceptions.RoleNameException())

        if len(role.permissions) < 1:
            logger.error("Try to create a rol with no permissions")
            return ServiceResult(RoleExceptions.RolePermissionsException())

        for permission in role.permissions:
            if not await verify_permissions(permission):
                logger.error("Invalid permission name in permissions")
                return ServiceResult(RoleExceptions.PermissionNameException())

        role_in_db = await RoleRepository(self.db).get_role_by_name(role.role)
        if role_in_db:
            logger.error("El nombre de rol ({role.role}) ya ha sido usado")
            return ServiceResult(RoleExceptions.RoleAlreadyExistsExcepton())

        role_item = await RoleRepository(self.db).create_role(role)

        if not role_item:
            logger.error("Error in DB creating a role")
            return ServiceResult(RoleExceptions.RoleCreateExcepton())

        return ServiceResult(role_item)

    async def get_roles_list(
        self,
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        roles = await RoleRepository(self.db).get_roles_list(search, order, direction)

        service_result = None
        if len(roles) == 0:
            logger.info("La lista de roles solicitada está vacía")
            roles_list = []
            service_result = ServiceResult(roles_list)
            service_result.status_code = 204
        else:
            # roles_list = [RoleOutList(**item.dict()) for item in roles]
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=roles,
                route=f"{config.API_PREFIX}/users/roles/",
            )
            service_result = ServiceResult(response)

        return service_result

    async def get_role_by_id(
        self,
        id: UUID,
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(RoleExceptions.RoleIdNoValidException())

        role = await RoleRepository(self.db).get_role_by_id(id=id)
        if isinstance(role, dict) and not role.get("id"):
            logger.info("El rol solicitado no está en base de datos")
            return ServiceResult(RoleExceptions.RoleNotFoundException())

        return ServiceResult(role)

    async def update_role(
        self, id: UUID, role_update: RoleUpdate, current_user_id: UUID
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(RoleExceptions.RoleIdNoValidException())

        try:
            role = await RoleRepository(self.db).update_role(
                id=id, role_update=role_update, updated_by_id=current_user_id
            )

            if isinstance(role, dict) and not role.get("id"):
                logger.info("El rol a actualizar no está en base de datos")
                return ServiceResult(RoleExceptions.RoleNotFoundException())

            return ServiceResult(role)

        except Exception:
            return ServiceResult(RoleExceptions.RoleInvalidUpdateParamsException())

    async def update_activate_role(
        self,
        id: UUID,
        role_update: RoleUpdateActive,
        current_user_id: UUID,
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(RoleExceptions.RoleIdNoValidException())

        if not role_update.is_active:
            if await self.verify_there_are_users_with_role(role_id=id):
                return ServiceResult(RoleExceptions.UsersUsingRoleException())

        role = await RoleRepository(self.db).update_active_role(
            id=id, role_update=role_update, updated_by_id=current_user_id
        )

        if isinstance(role, dict) and not role.get("id"):
            logger.info("El rol a actualizar no está en base de datos")
            return ServiceResult(RoleExceptions.RoleNotFoundException())

        return ServiceResult(role)

    async def delete_role(
        self,
        id: UUID,
        current_user: UserInDB,
    ) -> ServiceResult:
        if not is_valid_uuid(id):
            return ServiceResult(RoleExceptions.RoleIdNoValidException())

        if await self.verify_there_are_users_with_role(role_id=id):
            return ServiceResult(RoleExceptions.UsersUsingRoleException())

        role_id = await RoleRepository(self.db).delete_role(id=id)

        if isinstance(role_id, dict) and not role_id:
            logger.info("El rol a eliminar no está en base de datos")
            return ServiceResult(RoleExceptions.RoleNotFoundException())

        return ServiceResult(role_id)

    ###### INTERNAL UTILS FUNCTIONS #######
    async def verify_there_are_users_with_role(self, role_id: UUID) -> bool:
        users = await UserRepository(self.db).get_users_by_role_id(role_id)

        result: bool = False
        if not users or len(users) == 0:
            result = False

        if len(users) > 0:
            result = True

        return result
