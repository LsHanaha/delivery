from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    location_size_min: int = 1
    location_size_max: int = 10


settings = Settings()
