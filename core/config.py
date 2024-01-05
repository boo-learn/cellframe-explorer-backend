from pydantic import (
    BaseModel,
    ValidationError,
)

from pydantic_settings import (
    BaseSettings,
)


# class DatabaseConfig(BaseModel):
#     db_host: str
#     db_port: int = 5432


class Settings(BaseSettings):
    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        # env_prefix = "MYAPI_"
        env_nested_delimiter = "__"
        case_sensitive = False
        extra = 'allow'


settings = Settings()
