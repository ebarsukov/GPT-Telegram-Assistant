"""
model
"""
from pydantic import BaseModel


class MessageModel(BaseModel):
    """Buffer message model"""

    chat_id: int
    user_name: str
    text: str
    timestamp: float
    command: str | None = None


class GptSessionModel(BaseModel):
    """ChatGPT session model"""

    messages: list
    start_time: float
    last_msg_time: float
