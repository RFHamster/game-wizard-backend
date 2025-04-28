from dotenv import load_dotenv
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_ignore_empty=True,
        extra='ignore',
    )

    LLM_LLAMA_33_70B_INSTRUCT: str = 'meta/llama-3.3-70b-instruct'

    NVIDIA_NIM_API_KEY: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str

    BUCKET_NAME: str = 'game-wizard'

    QDRANT_SERVER_URL: str

    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: str = 'i6#b1HDL&9'
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = 'postgres'

    KAFKA_IP: str
    KAFKA_TOPIC: str = 'ingest-documents'

    @computed_field
    @property
    def sqlalchemy_db_uri(self) -> PostgresDsn:
        return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


settings = Settings()
