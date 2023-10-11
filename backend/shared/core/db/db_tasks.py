import os

from databases import Database
from fastapi import FastAPI
from loguru import logger
from modules.users.roles.role_schemas import RoleOut

# from modules.users.users.user_repositories import UserRepository
from shared.core import config


async def connect_to_db(app: FastAPI) -> None:
    try:
        DB_URL = (
            f"{config.DATABASE_URL}_test"
            if os.environ.get("TESTING")
            else config.DATABASE_URL
        )

        database = Database(
            DB_URL, min_size=config.DB_MIN_SIZE, max_size=config.DB_MAX_SIZE
        )

        await database.connect()
        app.state._db = database

        await verify_super_admin(db=database)

        logger.info("Database connection - successful")
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()  # database.disconnect()
        logger.info("Database connection - closed")
    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")


async def verify_super_admin(db: Database) -> None:
    from modules.users.users.user_repositories import UserRepository

    try:
        super = await UserRepository(db).get_user_by_username(config.SUPER_ADMIN)
        if not super:
            await _create_super_admin(db)
    except Exception as e:
        logger.error(f"se produjo este error: {e}")


async def _create_super_admin(db: Database) -> None:
    from modules.users.auths.auth_services import AuthService
    from modules.users.users.user_repositories import UserRepository
    from modules.users.users.user_schemas import UserIn

    role = await _verify_super_role(db)
    super_admin = UserIn(
        fullname=config.SUPER_ADMIN,
        username=config.SUPER_ADMIN,
        email=config.SUPER_EMAIL,
        password=config.SUPER_PASSWORD,
        is_superadmin=True,
        role_id=role.id,
    )

    user_password_update = AuthService().create_salt_and_hashedpassword(
        plaintext_password=super_admin.password
    )
    super_admin.password = user_password_update.password
    super_admin.salt = user_password_update.salt

    await UserRepository(db).create_user(super_admin)


async def _verify_super_role(db: Database) -> RoleOut:
    from modules.users.roles.role_repositories import RoleRepository

    role = await RoleRepository(db).get_role_by_name(config.SUPER_ROLE)
    if not role:
        role = await _create_super_role(db=db)

    return role


async def _create_super_role(db: Database) -> RoleOut:
    from modules.users.roles.role_repositories import RoleRepository
    from modules.users.roles.role_schemas import RoleIn

    role_in = RoleIn(role=config.SUPER_ROLE, permissions=[config.SUPER_PERMISO])
    return await RoleRepository(db).create_role(role_in)
