import logging
import os

from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    app_title: str = 'UrlsApp'
    project_name: str = 'library'
    project_host: str = '0.0.0.0'
    project_port: int = 8000
    database_dsn: PostgresDsn = os.getenv('DATABASE_DSN')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BLACK_LIST = []
    DB_WAS_PING = 'The database was ping'
    USER_REGISTER = 'User register request'
    USER_AUTH = 'User authentication request'
    NAME_EXISTS = 'This name already exists'
    USER_CREATED = 'User {name} created!'
    INVALID_NAME_OR_PASS = 'Invalid username or password'
    TOKEN_WAS_GENERATED = 'Auth token was generated!'
    UNATHORIZED = 'Unauthorized'
    DEFAULT_FILES_FOLDER = 'files'
    FILE_NOT_EXIST = 'The file "{filename}" on the path "{path}" does not exist'
    ZIP_FORMAT = 'zip'
    TYPE_OCTET_STREAM = 'application/octet-stream'
    DOT = '.'
    NO_ACCESS = 'No access'
    DB_CONNECTION = 'DB connection'

    class Config:
        env_file = '.env'

    class Logger:
        LOGGER_NAME = 'logger'
        ENCODING_UTF = 'utf-8'

        wb_logger = logging.getLogger(LOGGER_NAME)
        wb_handler = logging.FileHandler('loggs.log', 'a', ENCODING_UTF)
        wb_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        wb_logger.setLevel(logging.INFO)
        wb_logger.addHandler(wb_handler)
        wb_handler.setFormatter(wb_formatter)


app_settings = AppSettings()
