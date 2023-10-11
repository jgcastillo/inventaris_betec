from typing import Dict, List
from uuid import UUID

from loguru import logger
from modules.users.permissions import get_permissions
from modules.users.roles.role_exceptions import RoleExceptions
from modules.users.roles.role_schemas import (
    RoleIn,
    RoleOut,
    RoleOutList,
    RoleUpdate,
    RoleUpdateActive,
)
from shared.core.db.db_session_mixing import AppRepository


class RoleRepository(AppRepository):
    async def create_role(self, role: RoleIn) -> RoleOut:
        from modules.users.roles.role_sqlstatements import CREATE_ROLE

        values = self.preprocess_create(role.dict())
        role_record = await self.db.fetch_one(query=CREATE_ROLE, values=values)

        return RoleOut(**dict(role_record))

    async def get_role_by_name(self, role: str) -> RoleOut:
        from modules.users.roles.role_sqlstatements import GET_ROLE_BY_NAME

        values = {"role": role}
        record = await self.db.fetch_one(query=GET_ROLE_BY_NAME, values=values)

        if not record:
            return None

        return RoleOut(**dict(record))

    async def get_roles_list(
        self,
        search: str | None,
        order: str | None,
        direction: str | None,
    ) -> List[RoleOutList]:
        from modules.users.roles.role_sqlstatements import (
            GET_ROLES_LIST,
            GET_ROLES_LIST_FUNCTIONALITY,
            role_list_search,
            role_list_sort,
        )

        order = order.lower() if order != None else None
        direction = direction.upper() if direction != None else None
        values = {}
        sql_sentence = ""
        sql_sort = role_list_sort(order, direction)
        sql_search = role_list_search()

        results = []
        if not search:
            sql_sentence = GET_ROLES_LIST + sql_sort
            records = await self.db.fetch_all(query=sql_sentence, values=values)
        else:
            found = await self.__check_functionality(search.upper())
            if len(found) > 0:
                permit_list = await self.__get_permits(found)
                for permit in permit_list:
                    values["permit"] = permit
                    sql_sentence = GET_ROLES_LIST_FUNCTIONALITY + sql_sort

                    records_in_db = await self.db.fetch_all(
                        query=sql_sentence, values=values
                    )
                    results.extend(records_in_db)

                temp = [dict(record) for record in results]
                records = []
                [records.append(role) for role in temp if role not in records]
            else:
                sql_sentence = GET_ROLES_LIST + sql_search + sql_sort
                values["search"] = "%" + search.lower() + "%"
                records = await self.db.fetch_all(query=sql_sentence, values=values)

        if len(records) == 0:
            return []

        if not records:
            return []

        return [RoleOutList(**dict(record)) for record in records]

    async def get_role_by_id(self, id: UUID) -> RoleOut | dict:
        from modules.users.roles.role_sqlstatements import GET_ROLE_BY_ID

        values = {"id": id}
        record = await self.db.fetch_one(query=GET_ROLE_BY_ID, values=values)
        if not record:
            return {}

        return RoleOut(**dict(record))

    async def update_role(
        self, id: UUID, role_update: RoleUpdate, updated_by_id: UUID
    ) -> RoleOut | dict:
        from modules.users.roles.role_sqlstatements import UPDATE_ROLE_BY_ID

        role: RoleOut | Dict = await self.get_role_by_id(id=id)
        if not role:
            return {}

        role.updated_by = updated_by_id
        role.updated_at = self._preprocess_date()
        role_update_params = role.copy(update=role_update.dict(exclude_unset=True))

        try:
            record = await self.db.fetch_one(
                query=UPDATE_ROLE_BY_ID, values=role_update_params.dict()
            )
            role_in_db = dict(record)
            return RoleOut(**role_in_db)
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar un rol: {e}")
            raise RoleExceptions.RoleInvalidUpdateParamsException()

    async def update_active_role(
        self, id: UUID, role_update: RoleUpdateActive, updated_by_id: UUID
    ) -> RoleOut | dict:
        #  arreglar de aqui para abajo:
        from modules.users.roles.role_sqlstatements import UPDATE_ROLE_BY_ID

        role = await self.get_role_by_id(id=id)
        if not role:
            return {}

        role.updated_by = updated_by_id
        role.updated_at = self._preprocess_date()
        role_update_params = role.copy(update=role_update.dict(exclude_unset=True))

        try:
            record = await self.db.fetch_one(
                query=UPDATE_ROLE_BY_ID, values=role_update_params.dict()
            )
            return RoleOut(**dict(record))
        except Exception as e:
            logger.error(f"Datos inválidos para actualizar un rol: {e}")
            raise RoleExceptions.RoleInvalidUpdateParamsException()

    async def delete_role(
        self,
        id: UUID,
    ) -> str | dict:
        from modules.users.roles.role_sqlstatements import DELETE_ROLE_BY_ID

        role = await self.get_role_by_id(id=id)
        if not role:
            return {}

        deleted_id = await self.db.execute(query=DELETE_ROLE_BY_ID, values={"id": id})
        return str(deleted_id)

    ####### INTERNAL UITILS ########
    async def __check_functionality(self, search: str) -> str:
        functionalities = await self.__get_functionalities()
        for funct in functionalities:
            if funct.find(search) >= 0:
                return funct

        return ""

    async def __get_functionalities(self):
        permissions = await get_permissions()
        funct_list = []
        for dic in permissions:
            funct_list.append(dic.get("functionality"))

        return funct_list

    async def __get_permits(self, search: str):
        permissions = await get_permissions()
        funct_routes = []
        for dic in permissions:
            if dic["functionality"] == search:
                funct_routes = dic["routes"]
                break

        permits = []
        if len(funct_routes) > 0:
            permits = [next(iter(dic)) for dic in funct_routes]
            # for dic in funct_routes:
            #     permits.append(next(iter(dic)))
        return permits
