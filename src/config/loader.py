import os
from typing import Union, TypeVar

def load_dotenv(filepath: str = ".env"):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip() # remove \n, white space
            if line: # if line exist
                line_token = line.split("=") # split assign operator
                key = line_token[0].strip()
                value = line_token[1].strip()
                os.environ[key] = value

T = TypeVar('T')
def get_env(key: str, default: T = None) -> Union[str, T]:
    return os.environ.get(key, default)