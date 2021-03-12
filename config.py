import os

class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "1630473786:AAGUZAykO3lfl1_2FJLGc3YsaGvpuFKILS8")
    API_HASH = os.environ.get("API_HASH", "dc38616c85d4df82970c7178f3205c6f")
    API_ID = int(os.environ.get("APP_ID", 1555934))