from datetime import datetime
from typing import Type
from uuid import uuid4

from databases import Database
from loguru import logger
from modules.users.users.user_repositories import UserRepository
from modules.users.users.user_schemas import UserInDB
from shared.core.db.db_session_mixing import AppRepository


class AuthRepository(AppRepository):
    async def authenticate_user(self, username: str) -> UserInDB | None:
        user_repo = UserRepository(self.db)
        user = await user_repo.get_user_by_username(username=username)

        if not user:
            return None

        return user

    async def save_token_used(self, token: str) -> dict:
        from modules.users.auths.auth_sqlstatements import SAVE_TOKEN

        values = {"id": uuid4(), "token": token, "created_at": datetime.now()}
        record = await self.db.fetch_one(query=SAVE_TOKEN, values=values)

        return dict(record)

    async def get_token_by_value(self, token: str) -> dict:
        from modules.users.auths.auth_sqlstatements import GET_TOKEN_BY_VALUE

        values = {"token": token}
        record = await self.db.fetch_one(query=GET_TOKEN_BY_VALUE, values=values)

        if not record:
            return {}

        return dict(record)
