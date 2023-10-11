from modules.users.users.user_schemas import UserInDB
from shared.utils.service_result import ServiceResult, handle_result


def is_authorized(current_user: UserInDB, endpoint: str) -> bool:
    if current_user.is_superadmin or endpoint in current_user.permissions:
        return True
    else:
        return False
