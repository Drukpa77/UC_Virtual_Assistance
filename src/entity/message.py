from src.db import BaseModel
from src.db.types import Text, Boolean, String

class Message(BaseModel):
    __table_name__ = "message"

    session = String()
    message = Text()
    is_bot = Boolean()