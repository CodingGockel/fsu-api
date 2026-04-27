from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    moodle_password: str
    moodle_username: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
settings = Settings() # type: ignore 