from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    API_REST_URL: str = 'http://localhost:8000/cards'
    QUEUES: list[str] = ['queue_a', 'queue_b', 'queue_c']
    RABBITMQ_URL: str = 'amqp://user:password@localhost:5672/'


ENV = Settings()