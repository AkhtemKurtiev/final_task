from pydantic_settings import BaseSettings

from src.shemas.authJWT import AuthJWT


class Settings(BaseSettings):
    api_v1_prefix: str = '/api/v1'
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
