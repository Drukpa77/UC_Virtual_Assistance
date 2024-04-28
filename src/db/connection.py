from src.config import get_env
import psycopg2 as database
from .constant import *

def db_connect():
    con = database.connect(database=get_env(ENV_DB_DATABASE),
                    host=get_env(ENV_DB_HOST),
                    user=get_env(ENV_DB_USER))
    return con