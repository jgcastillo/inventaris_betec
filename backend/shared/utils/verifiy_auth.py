# from modules.integrations.authentications.authentications_schemas import AuthInDB
from modules.api_auth.api_auth_schemas import AuthInDB
from modules.users.users.user_schemas import UserInDB


def is_authorized(current_user: UserInDB, endpoint: str) -> bool:
    if current_user.is_superadmin or endpoint in current_user.permissions:
        return True
    else:
        return False


def api_key_active(api_key: AuthInDB) -> bool:
    if api_key.is_active == True:
        return True
    else:
        return False
