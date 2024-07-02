from dotenv import load_dotenv
from pydantic import SecretStr
import os

from pydantic.v1 import BaseSettings

load_dotenv()


class DevSettings(BaseSettings):
    influx_url: str = os.getenv("INFLUXDB_URL")
    influx_token: str = os.getenv("INFLUXDB_TOKEN")
    influx_org: str = os.getenv("INFLUXDB_ORG")
    influx_bucket: str = os.getenv("INFLUXDB_BUCKET")

    mongo_furl: str = os.getenv("MONGO_FURL")


# environment = os.getenv('ENVIRONMENT')


environment = 'dev'


class ProdSettings:
    pass


if environment == 'dev':
    settings = DevSettings()
elif environment == 'prod':
    settings = ProdSettings()
