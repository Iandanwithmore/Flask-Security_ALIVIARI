class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "BatmanisBruceWayne"

    LOG_FILE = "/var/log/front_server.log"

    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "csv"}
    MAX_CONTENT_LENGTH = 16000
    PATH_FILE = "mnt/Docs/PACIENTE"

    APP_PORT = "8001"
    API_URL = "http://127.0.0.1:4000"

    SECURE = True
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    RSA_PUBLIC = None
    RSA_PRIVATE = None

    # REDIS_URL = "redis://localhost:6379"
    # REDIS_HOST = "localhost"
    # REDIS_PORT = 6379
    # REDIS_DB = ""
    # REDIS_PASSWORD = ""

    # app.config['SESSION_TYPE'] = 'redis'
    # app.config['SESSION_PERMANENT'] = False
    # app.config['SESSION_USE_SIGNER'] = True
    # app.config['SESSION_REDIS'] = redis.from_url(os.environ['REDIS_URL'])


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_FILE = "log/front_dev.log"

    PATH_FILE = "C:/xampp/htdocs/CLANAD/Docs/PACIENTE"

    SECURE = False


class TestingConfig(Config):
    TESTING = True
    LOG_FILE = "log/front_test.log"

    PATH_FILE = "C:/xampp/htdocs/CLANAD/Docs/PACIENTE"

    SECURE = False
