from .loader import get_env

class EnvConfig:
    def __init__(self) -> None:
        self.bm25_model = "./outputs/bm25"
        self.document_model = "./outputs/document"
        self.DB_HOST = get_env("DB_HOST")
        self.DB_USER = get_env("DB_USER")
        self.DB_DATABASE = get_env("DB_DATABASE")
        self.DB_PORT = get_env("DB_PORT")