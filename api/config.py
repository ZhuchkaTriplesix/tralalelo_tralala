from abc import ABC
from dataclasses import asdict, dataclass
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


class CfgBase(ABC):
    dict: callable = asdict


class PostgresCfg(CfgBase):
    def __init__(self):
        self.database: str = config["POSTGRES"]["DATABASE"]
        self.driver: str = config["POSTGRES"]["DRIVER"]
        self.database_name: str = config["POSTGRES"]["DATABASE_NAME"]
        self.username: str = config["POSTGRES"]["USERNAME"]
        self.password: str = config["POSTGRES"]["PASSWORD"]
        self.ip: str = config["POSTGRES"]["IP"]
        self.port: int = config.getint("POSTGRES", "PORT")

    @property
    def url(self) -> str:
        return (f"{self.database}+{self.driver}://{self.username}:{self.password}@{self.ip}:{self.port}/"
                f"{self.database_name}")


@dataclass
class UvicornCfg(CfgBase):
    host: str = config["UVICORN"]["HOST"]
    port: int = config.getint("UVICORN", "PORT")


@dataclass
class RedisCfg(CfgBase):
    host: str = config["REDIS"]["HOST"]
    port: int = config.getint("REDIS", "PORT")
    db: int = config.getint("REDIS", "DB")
    password: str = config["REDIS"]["PASSWORD"]


uvicorn = UvicornCfg()
postgres = PostgresCfg()
redis = RedisCfg()
