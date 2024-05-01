from .loader import get_env

class EnvConfig:
    def __init__(self) -> None:
        self.bm25_model = get_env("BM25_MODEL")
        self.document_model = get_env("PAIRWISE_MODEL")
        self.HF_MODEL = get_env("HF_MODEL")
        self.DB_HOST = get_env("DB_HOST")
        self.DB_USER = get_env("DB_USER")
        self.DB_DATABASE = get_env("DB_DATABASE")
        self.DB_PORT = get_env("DB_PORT")
        self.REDIS_HOST = get_env("REDIS_HOST")
        self.REDIS_PORT = get_env("REDIS_PORT")