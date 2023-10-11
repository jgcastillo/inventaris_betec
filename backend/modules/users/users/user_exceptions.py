from typing import Any

from shared.utils.app_exceptions import AppExceptionCase


class UserExceptions:
    class UserCreateExcepton(AppExceptionCase):
        """_
        User creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 500
            context = {"mensaje": "Error creando usuario"}
            AppExceptionCase.__init__(self, status_code, context)

    class UserWithNoRoleException(AppExceptionCase):
        """_
        User with no rol creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "Usuario debe tener un rol"}
            AppExceptionCase.__init__(self, status_code, context)

    class UserWithNoUsernameException(AppExceptionCase):
        """_
        User with no rol creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "Usuario debe tener un nombre de usario (username)"}
            AppExceptionCase.__init__(self, status_code, context)

    class UserWithNoValidEmailException(AppExceptionCase):
        """_
        User with no rol creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "Usuario debe tener un correo valido"}
            AppExceptionCase.__init__(self, status_code, context)

    class UserWithNoValidPasswordException(AppExceptionCase):
        """_
        User with no rol creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "Usuario debe tener un password valido"}
            AppExceptionCase.__init__(self, status_code, context)

    class UserWithNoUserTypeException(AppExceptionCase):
        """_
        User with no rol creation failed
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "Usuario debe indicar tipo de usuario"}
            AppExceptionCase.__init__(self, status_code, context)

    class UserEmailAlreadyExistsExeption(AppExceptionCase):
        """_
        User email already exists
        """

        def __init__(self, context: dict = None):
            status_code = 400
            context = {"mensaje": "Email de usuario ya existe"}
            AppExceptionCase.__init__(self, status_code, context)

    class UserUsernameAlreadyExistsExeption(AppExceptionCase):
        """_
        User email already exists
        """

        def __init__(self, context: dict = None):
            status_code = 400
            context = {"mensaje": "Nombre de usuario (username) ya existe"}
            AppExceptionCase.__init__(self, status_code, context)

    class UsersListsException(AppExceptionCase):
        """
        Could not recover uasers list
        """

        def __init__(self, context: dict = None):
            status_code = 500
            context = {"mensaje": "No se pudo recuperar la lista de usuarios"}
            AppExceptionCase.__init__(self, status_code, context)

    class UserNotFoundException(AppExceptionCase):
        """_
        User not found
        """

        def __init__(self, context: dict = None):
            status_code = 404
            context = {"mensaje": "Id de usuario no encontrado"}
            AppExceptionCase.__init__(self, status_code, context)

    class UserInvalidUpdateParamsException(AppExceptionCase):
        """_
        User Invalid update parameters
        """

        def __init__(self, context: dict = None, e: Any = None):
            self.error = e
            status_code = 422
            context = {
                "mensaje": f"Parámetros de actualización inválidos",
                "error": str(self.error),
            }
            AppExceptionCase.__init__(self, status_code, context)

    class UserIdNoValidException(AppExceptionCase):
        """_
        User Id invalid
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"mensaje": "Id de usuario inválido"}
            AppExceptionCase.__init__(self, status_code, context)

    class CanNotChangePswOfOtherUserException(AppExceptionCase):
        """_
        User can not chandge the password of other user
        """

        def __init__(self, context: dict = None):
            status_code = 409
            context = {"mensaje": "No puede cambiar el password de otro usuario"}
            AppExceptionCase.__init__(self, status_code, context)
