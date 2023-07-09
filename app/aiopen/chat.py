"""
aiopen.chatgpt
"""
import threading
import sys
import time
import openai
from loguru import logger
from conf import conf
from model import GptSessionModel, MessageModel
from buffer import (
    telegram_to_gpt_buffer,
    gpt_to_telegram_buffer,
    del_obsolete_buffer_msg,
)


openai.api_key = conf.environment.OPENAI_API_KEY

OPENAI_MODEL = conf.environment.OPENAI_API_MODEL
OPENAI_CHAT_LIFETIME_SEC = int(conf.environment.OPENAI_CHAT_LIFETIME_SEC)
OPENAI_TEMPERATURE = float(conf.environment.OPENAI_TEMPERATURE)
OPENAI_MAX_TOKENS = int(conf.environment.OPENAI_MAX_TOKENS)
OPENAI_CHAT_USER_PRESET = conf.environment.OPENAI_CHAT_USER_PRESET
OPENAI_CHAT_SYSTEM_PRESET = conf.environment.OPENAI_CHAT_SYSTEM_PRESET

MN = "[ChatGPT]"


class ChatAI:
    """ChatGPT"""

    def __init__(self):
        self._input_buffer = telegram_to_gpt_buffer
        self._output_buffer = gpt_to_telegram_buffer
        self._sessions = {}
        self.temperature = OPENAI_TEMPERATURE
        self.max_tokens = OPENAI_MAX_TOKENS

    def send_request(self, msg) -> MessageModel:
        """Send a request to chatGPT"""

        try:
            chat = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=self._create_session(msg),
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            msg.text = chat.choices[0].message.content

        except Exception as error:  # pylint: disable=broad-except
            err_msg = f"{MN} Error: {error}"
            logger.error(err_msg)
            msg.text = err_msg

        msg.timestamp = time.time()

        logger.debug(f"{MN} Response: {msg.chat_id=} {msg.user_name=} {msg.text=}")

        return msg

    def start(self):
        """Start the chat thread"""
        thr = threading.Thread(target=self._loop, args=(threading.current_thread(),))
        thr.start()

    def _loop(self, main_thread):
        logger.info(f"{MN} Thread started ...")
        while True:
            if not main_thread.is_alive():
                logger.info(f"{MN} Thread stopped")
                sys.exit()
            time.sleep(0.1)
            self._input_buffer_handling()
            self._del_obsolete_sessions()
            del_obsolete_buffer_msg(MN, self._output_buffer)

    def _create_session(self, msg) -> None:
        if not msg.chat_id in self._sessions:
            sys_peset = OPENAI_CHAT_SYSTEM_PRESET.replace("{user_name}", msg.user_name)

            chat = [{"role": "system", "content": sys_peset}]

            if OPENAI_CHAT_USER_PRESET:
                chat.append({"role": "user", "content": OPENAI_CHAT_USER_PRESET})

            self._sessions[msg.chat_id] = GptSessionModel(
                messages=chat,
                start_time=time.time(),
                last_msg_time=time.time(),
            )
            logger.debug(f"{MN} Make new session: {msg.chat_id=}")

        self._sessions[msg.chat_id].messages.append(
            {"role": "user", "content": msg.text}
        )

        return self._sessions[msg.chat_id].messages

    def _delete_session(self, chat_id) -> None:
        if chat_id in self._sessions:
            self._sessions.pop(chat_id, None)
            logger.debug(f"{MN} Deleted session: {chat_id=}")

    def _del_obsolete_sessions(self) -> None:
        for key, body in self._sessions.items():
            if time.time() - body.last_msg_time > OPENAI_CHAT_LIFETIME_SEC:
                self._sessions.pop(key, None)
                logger.debug(f"{MN} Session live timeout ended: chat_id={key}")
                return

    def _del_obsolete_output_buffer_msg(self) -> None:
        for num, msg in enumerate(self._output_buffer):
            if time.time() - msg.timestamp > OPENAI_CHAT_LIFETIME_SEC:
                self._output_buffer.pop(num)
                logger.warning(
                    f"{MN} Delet obsolete outbut buffer msg: "
                    + f"chat_id={msg.chat_id=} {msg.user_name=} {msg.text=}"
                )
                return

    def _run_command(self, msg) -> None:
        logger.debug(f"{MN} Command: {msg.chat_id=} {msg.user_name=} {msg.command=}")
        match msg.command:
            case "new_session":
                self._delete_session(msg.chat_id)
                msg.text = "New session started..."
                msg.timestamp = time.time()
                self._output_buffer.append(msg)

    def _input_buffer_handling(self):
        if not self._input_buffer:
            return

        msg = self._input_buffer[0]
        self._input_buffer.pop(0)

        if msg.command:
            self._run_command(msg)
            return

        self._output_buffer.append(self.send_request(msg))
