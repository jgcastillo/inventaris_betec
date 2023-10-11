from shared.utils.app_exceptions import AppExceptionCase


class PermissionsExceptions:
    class PermissionsListException(AppExceptionCase):
        """_
        Permissions list failed
        """

        def __init__(self, context: dict = None):
            status_code = 500
            context = {"mensaje": "No tiene permiso para ver esta lista"}
            AppExceptionCase.__init__(self, status_code, context)

    class PermissionsEmptyListException(AppExceptionCase):
        """_
        Permissions list failed
        """

        def __init__(self, context: dict = None):
            status_code = 204
            context = {"mensaje": "Lista vacía"}
            AppExceptionCase.__init__(self, status_code, context)
