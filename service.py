import os
from dotenv import load_dotenv


class ENV:
    def __init__(self):
        load_dotenv()
        self.token_bot = os.getenv("TOKEN_BOT")
        self.my_channel = os.getenv("MY_CHANNEL")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT")


token_env = ENV()