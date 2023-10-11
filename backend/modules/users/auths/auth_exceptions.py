from shared.utils.app_exceptions import AppExceptionCase


class AuthExceptions:
    class AuthNoUsernameException(AppExceptionCase):
        """_
        Auth no username
        """

        def __init__(self, context: dict = {}):
            status_code = 422
            context = {"message": "No se ha ingresado un nombre de usuario"}
            AppExceptionCase.__init__(self, status_code, context)

    class AuthNoPasswordException(AppExceptionCase):
        """_
        Auth no password
        """

        def __init__(self, context: dict = None):
            status_code = 422
            context = {"message": "No se ha ingresado una clave de ingreso"}
            AppExceptionCase.__init__(self, status_code, context)

    class AuthNoValidCredencialsException(AppExceptionCase):
        """_
        Auth no valid credentials
        """

        def __init__(self, context: dict = None):
            status_code = 401
            context = {"message": "Credenciales no válidas"}
            AppExceptionCase.__init__(self, status_code, context)

    class AuthNoValidTokenCredentialsException(AppExceptionCase):
        """_
        Auth no valid credentials
        """

        def __init__(self, context: dict = None):
            status_code = 401
            context = {"message": "No se pudo validar el token"}
            AppExceptionCase.__init__(self, status_code, context)

    class AuthUnauthorizedException(AppExceptionCase):
        """
        No access authorization
        """

        def __init__(self, context: dict = None):
            status_code = 401
            context = {"message": "No está autorizado para ejecutar esta función"}
            AppExceptionCase.__init__(self, status_code, context)

    class AuthTokenExpiredException(AppExceptionCase):
        """_
        Auth no valid credentials
        """

        def __init__(self, context: dict = None):
            status_code = 401
            context = {
                "mensaje": "EL tiempo de su sessión ha expirado, por favor vuelva a ingresar"
            }
            AppExceptionCase.__init__(self, status_code, context)

    class AuthRestPswTokenExpiredException(AppExceptionCase):
        """_
        Token de reset de passwaord está vencido
        """

        def __init__(self, context: dict = None):
            status_code = 400
            context = {
                "message": "El tiempo de renovación de la clave ha vencido, vuelva a intentarlo"
            }
            AppExceptionCase.__init__(self, status_code, context)

    class AuthRestPswTokenUsedException(AppExceptionCase):
        """_
        Token de reset de passwaord ha sido usado
        """

        def __init__(self, context: dict = None):
            status_code = 400
            context = {"message": "No se pudo validar el token"}
            AppExceptionCase.__init__(self, status_code, context)
