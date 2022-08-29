from conf.settings.base import Settings


class ProdAppSettings(Settings):
    debug: bool = False

    class Config(Settings.Config):
        env_file = "prod.env"
        env_file_encoding = 'utf-8'
