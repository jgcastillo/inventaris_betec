import os
from typing import Optional

from databases import DatabaseURL
from pydantic import PostgresDsn
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "INVENTARIS"
DESCRIPTION = "Sistema de Gestión de Administrativa de Betecnica"
DEBUG: bool = False
TIMEZONE: str = "America/Caracas"

VERSION = "1.0.0"
API_PREFIX = "/api/v1"

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

# superuser credentials
SUPER_ADMIN = config("SUPER_ADMIN", cast=str)
SUPER_PASSWORD = config("SUPER_PASSWORD", cast=str)
SUPER_EMAIL = config("SUPER_EMAIL", cast=str)
SUPER_ROLE = config("SUPER_ROLE", cast=str)
SUPER_PERMISO = config("SUPER_PERMISO", cast=str)

# auth and jwt
SECRET_KEY = config("SECRET_KEY", cast=Secret)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str)
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str)
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str)
AES_KEY = config("AES_KEY", cast=str)
AES_BLOCKSIZE = config("AES_BLOCKSIZE", cast=int)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}",
)


DB_MIN_SIZE: int = 2
DB_MAX_SIZE: int = 15
DB_FORCE_ROLL_BACK: bool = False

# locations api
LOCATIONS_URL = config("LOCATIONS_URL", cast=str)
CURRENT_COUNTRY = config("CURRENT_COUNTRY", cast=str)

# AWS access
# AWS_ACCESS_KEY = config("AWS_ACCESS_KEY", cast=str)
# AWS_ACCESS_SECRET = config("AWS_ACCESS_SECRET", cast=str)
# S3_BUCKET_NAME = config("S3_BUCKET_NAME", cast=str)
# S3_BUCKET_BASE_URL = config("S3_BUCKET_BASE_URL", cast=str)
# BUCKET_REGION = config("BUCKET_REGION", cast=str)

# email api
SENDGRID_API_KEY = config("SENDGRID_API_KEY", cast=str)
NO_RESPOND_EMAIL_ADDRESS = config("NO_RESPOND_EMAIL_ADDRESS", cast=str)
EMAIL_RESET_TOKEN_EXPIRE_MINUTES = config("EMAIL_RESET_TOKEN_EXPIRE_MINUTES", cast=int)
EMAIL_TEMPLATES_DIR = config("EMAIL_TEMPLATES_DIR", cast=str)
URL_CHANGE_PSW = config("URL_CHANGE_PSW", cast=str)

