"""
buffer
"""
import time
from loguru import logger
from conf import conf

MN = "[Message Buffer]"

BUFFER_MSG_LIFETIME_SEC = int(conf.environment.BUFFER_MSG_LIFETIME_SEC)

telegram_to_gpt_buffer = []
gpt_to_telegram_buffer = []


def del_obsolete_buffer_msg(mname, buffer) -> None:
    """Delete obsolete buffer message"""
    for num, msg in enumerate(buffer):
        if time.time() - msg.timestamp > BUFFER_MSG_LIFETIME_SEC:
            buffer(num)
            logger.warning(
                f"{mname} Delet obsolete outbut buffer msg: "
                + f"chat_id={msg.chat_id=} {msg.user_name=} {msg.text=}"
            )
            return
