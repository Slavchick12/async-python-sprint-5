import logging
import os

from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    app_title: str = 'UrlsApp'
    database_dsn: PostgresDsn = os.getenv('DATABASE_DSN')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BLACK_LIST = []
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'library')
    PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
    PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))
    DB_WAS_PING = 'The database was ping'
    DB_IS_OK = 'There is nothing wrong with the database'
    DB_WRONG_OR_EMPTY = 'There is something wrong with the database or it is empty'
    URLS_RECEIVED = 'All short non-deleted urls were received!'
    URL_NOT_FOUND = 'Url not found!'
    URL_WAS_DELETED = 'Url {url} was deleted!'
    URL_RECEIVED = 'Url {url} successfully received!'
    ENTRY_WAS_DELETED = 'Database entry with id={id} was deleted!'
    REQUEST_STATUS = 'Info request per url {url}'
    ALL_INFO_RECEIVED = 'All info per url {url} received'
    VISITS_RECEIVED = 'Visits per url {url} received'
    USER_REGISTER = 'User register request'
    USER_AUTH = 'User authentication request'
    NAME_EXISTS = 'This name already exists'
    USER_CREATED = 'User {name} created!'
    INVALID_NAME_OR_PASS = 'Invalid username or password'
    TOKEN_WAS_GENERATED = 'Auth token was generated!'
    UNATHORIZED = 'Unauthorized'
    DEFAULT_FILES_FOLDER = 'files'

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
