from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # These names must exactly match the keys in your .env file (case-insensitive)
    app_name: str = "Default API Name" # Provides a fallback default
    database_url: str                  # Required! App will crash on startup if missing
    secret_key: str                    # Required!
    debug: bool = False                # Automatically converts the string True to a boolean!

    # This tells Pydantic to look for a file named .env
    model_config = SettingsConfigDict(env_file=".env")

# We use @lru_cache so Python only reads the .env file from the hard drive ONCE,
# rather than re-reading it on every single API request (which slows down your app).
@lru_cache()
def get_settings():
    return Settings()