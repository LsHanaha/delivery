from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    location_size_min: int = 1
    location_size_max: int = 10

    db_dsn: str = "postgresql+asyncpg://username:password@localhost:5432/delivery"
    database_name: str = "delivery"
    database_connection_timeout: float = 10.0

    geo_dsn: str = "localhost:5004"


settings = Settings()
