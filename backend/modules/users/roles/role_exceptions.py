from shared.utils.app_exceptions import AppExceptionCase


class RoleExceptions:
    class RoleCreateExcepton(AppExceptionCase):
        """_
        Rol creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 500
            context = {"mensaje": "Error creando el rol"}
            AppExceptionCase.__init__(self, status_code, context)

    class RoleAlreadyExistsExcepton(AppExceptionCase):
        """_
        Rol already exists
        """

        def __init__(self, context: dict = None):
            status_code = 409
            context = {
                "mensaje": "El nombre del rol ya ha sido declarado anteriormente"
            }
            AppExceptionCase.__init__(self, status_code, context)

    class RoleNameException(AppExceptionCase):
        """_
        Rol creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "El rol debe tener un nombre"}
            AppExceptionCase.__init__(self, status_code, context)

    class RolePermissionsException(AppExceptionCase):
        """_
        Rol creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "Sin información de permisos"}
            AppExceptionCase.__init__(self, status_code, context)

    class RolesListsException(AppExceptionCase):
        """_
        Role list failed
        """

        def __init__(self, context: dict = None):
            status_code = 500
            context = {"mensaje": "No se pudo obtener la lista de roles"}
            AppExceptionCase.__init__(self, status_code, context)

    class RoleIdNoValidException(AppExceptionCase):
        """_
        Role id not valid
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "Id no está en formato aceptable"}
            AppExceptionCase.__init__(self, status_code, context)

    class RoleNotFoundException(AppExceptionCase):
        """_
        Role not found
        """

        def __init__(self, context: dict = None):
            status_code = 404
            context = {"mensaje": "No se ha encontrado un rol con el Id suministrado"}
            AppExceptionCase.__init__(self, status_code, context)

    class RoleInvalidUpdateParamsException(AppExceptionCase):
        """_
        Role with invalid params to update
        """

        def __init__(self, context: dict = None):
            status_code = 400
            context = {"mensaje": "Parámetros inválidos para actualizar un rol"}
            AppExceptionCase.__init__(self, status_code, context)

    class PermissionNameException(AppExceptionCase):
        """_
        Rol creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "Nombre de permiso ilegal en Permisos"}
            AppExceptionCase.__init__(self, status_code, context)

    class UsersUsingRoleException(AppExceptionCase):
        """_
        Rol can't be deactivate / delete because there are users
        with it
        """

        def __init__(self, context: dict = None):
            status_code = 409
            context = {
                "mensaje": "No se puede desactivar / eliminar este rol. Hay usuarios que lo usan"
            }
            AppExceptionCase.__init__(self, status_code, context)

    class CanNotDeactivateOrDeleteSuperAdmin(AppExceptionCase):
        """_
        SuperAdmin can't be deactivate / delete from the system
        with it
        """

        def __init__(self, context: dict = None):
            status_code = 409
            context = {
                "mensaje": "No se puede desactivar / eliminar al super administrador"
            }
            AppExceptionCase.__init__(self, status_code, context)
