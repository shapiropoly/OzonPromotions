from pydantic import SecretStr
from dotenv import dotenv_values


class Settings:
    def __init__(self):
        env = dotenv_values("token.env")
        self.bot_token = SecretStr(env.get("token"))


config = Settings()
