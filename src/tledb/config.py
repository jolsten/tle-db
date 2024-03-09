from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, FilePath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class SqliteDatabase(BaseModel):
    backend: Literal["sqlite"] = "sqlite"
    name: Union[Literal[":memory:"], FilePath] = None

    @property
    def url(self) -> URL:
        name = self.name if self.name else ":memory:"
        return URL.create(drivername="sqlite", database=name)


class MySQLDatabase(BaseModel):
    backend: Literal["mysql", "mariadb"] = "mysql"
    driver: Optional[Literal["pymysql"]] = None
    host: str
    port: int
    username: SecretStr
    password: SecretStr
    name: str

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=f"{self.backend}+{self.driver}",
            database=self.name,
            username=self.username.get_secret_value(),
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="TLEDB_",
        env_nested_delimiter="__",
    )

    database: Union[SqliteDatabase, MySQLDatabase] = Field(discriminator="backend")


settings = Settings()
