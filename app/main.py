"""
main
"""
from telegram import TeleBot
from aiopen import ChatAI


def main():
    """Program starting here"""
    ChatAI().start()
    TeleBot().start()


if __name__ == "__main__":
    main()
