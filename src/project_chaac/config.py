from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # don't error on unrelated env vars
    )

    # localhost default for running the worker from your terminal against
    # a Dockerized RabbitMQ. Compose will override this to amqp://...@rabbitmq...
    broker_url: str = "amqp://guest:guest@localhost:5672//"

    # --- mock auth (real version compares key against a partner registry) ---
    api_key: str = "dev-secret-key"
    # comma-separated in env; parsed to a list below
    allowed_ips: str = "127.0.0.1,::1,testclient"
    result_backend: str = "redis://localhost:6379/0"



# single shared instance — import this everywhere, never construct Settings() again
settings = Settings()