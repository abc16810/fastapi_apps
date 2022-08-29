from conf.settings.base import Settings



class DevAppSettings(Settings):
    debug: bool = True
    title: str = "Dev FastAPI example application"

    class Config(Settings.Config):
        env_file = ".env"   # python-dotenv
        env_file_encoding = 'utf-8'

