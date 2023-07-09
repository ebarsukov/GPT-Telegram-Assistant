"""
telegram.bot
"""
import threading
import time
import telebot
from loguru import logger
from model import MessageModel
from buffer import telegram_to_gpt_buffer, gpt_to_telegram_buffer
from config import conf

MN = "[Telebot]"
TIMEOUT = 20
TELEGRAM_BOT_TOKEN = conf.environment.TELEGRAM_BOT_TOKEN


def _error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:  # pylint: disable=broad-except
            logger.error(f"{MN} {err}")
            return False

    return wrapper


class TeleBot:
    """Telegram bot"""

    def __init__(self, token=TELEGRAM_BOT_TOKEN, timeout=TIMEOUT):
        self._parse_mode = None  # You can set parse_mode by default. HTML or MARKDOWN
        self._bot = telebot.TeleBot(token, threaded=True, parse_mode=self._parse_mode)
        self.timeout = timeout
        self._response_buffer = gpt_to_telegram_buffer
        self._request_buffer = telegram_to_gpt_buffer

    def start(self) -> None:
        """Run loop"""
        pull_thr = threading.Thread(target=self._polling_loop)
        pull_thr.start()
        while True:
            time.sleep(0.1)
            self._send_response_msg()

    def _send_response_msg(self):
        if not self._response_buffer:
            return
        msg = self._response_buffer[0]

        if self.send_text(msg.chat_id, msg.text):
            self._response_buffer.pop(0)
        else:
            time.sleep(10)

    @_error_handler
    def send_text(self, chat_id, text) -> bool:
        """Sending text to server"""
        self._bot.send_message(chat_id, text, parse_mode=self._parse_mode)
        logger.debug(f"{MN} Send msg: {chat_id=} {text=}")
        return True

    @_error_handler
    def send_photo(self, raw_img, chat_id, caption=None) -> bool:
        """Sending photo to server"""
        self._bot.send_photo(chat_id, raw_img, caption=caption)
        logger.debug(f"{MN} Send photo: {chat_id=}")
        return True

    def _polling_loop(self):
        logger.info(f"{MN} Polling thread started ...")
        while True:
            self._polling()
            time.sleep(10)

    @_error_handler
    def _polling(self) -> None:
        @self._bot.message_handler(commands=["new_session"])
        def cmd_new_session(message):
            self._add_msg_to_request_buffer(message, cmd="new_session")

        @self._bot.message_handler(content_types=["text"])
        def incoming_text(message):
            self._add_msg_to_request_buffer(message)

        # self._bot.infinity_polling(interval=0, timeout=TIMEOUT)
        self._bot.polling(interval=0, timeout=TIMEOUT)

    def _add_msg_to_request_buffer(self, message, cmd=None):
        chat_id = message.chat.id
        user_name = message.chat.first_name
        text = message.text

        logger.debug(f"{MN} Request: {chat_id=} {user_name=} {text=}")

        self._request_buffer.append(
            MessageModel(
                chat_id=chat_id,
                user_name=user_name,
                text=text,
                timestamp=time.time(),
                command=cmd,
            )
        )
