import os

from pydantic import BaseSettings

EOD_HISTORICAL_DATA_API_KEY_ENV_VAR = "EOD_HISTORICAL_API_KEY"
EOD_HISTORICAL_DATA_API_URL = 'https://eodhistoricaldata.com/api'


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    database_url: str = 'sqlite:///./db.sqlite3'

    eod_historical_data = {
        'API_TOKEN': os.getenv(EOD_HISTORICAL_DATA_API_KEY_ENV_VAR),
        'API_URL': EOD_HISTORICAL_DATA_API_URL
    }
    
    log_level = 'info'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
