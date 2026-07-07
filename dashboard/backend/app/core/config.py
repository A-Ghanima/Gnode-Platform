from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    DOCKER_SOCKET: str = "unix:///var/run/docker.sock"
    PROMETHEUS_URL: str = "http://prometheus:9090"
    LOKI_URL: str = "http://loki:3100"
    ALERTMANAGER_URL: str = "http://alertmanager:9093"

    class Config:
        env_file = ".env"

settings = Settings()
