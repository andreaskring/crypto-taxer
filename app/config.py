from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    ledger_path: Path


def get_settings() -> Settings:
    return Settings()
