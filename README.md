# GPT Telegram Asistant

[![GitHub top language](https://img.shields.io/github/languages/top/ebarsukov/gpt-telegram-assistant)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Stars](https://img.shields.io/github/stars/ebarsukov/gpt-telegram-assistant.svg?maxAge=86400)](https://github.com/ebarsukov/gpt-telegram-assistant)
[![Docker Pulls](https://img.shields.io/docker/pulls/edevai/gpt-telegram-asystant.svg?maxAge=86400)]()
[![Version](https://img.shields.io/github/release/ebarsukov/gpt-telegram-assistant?display_name=tag&sort=semver)](https://github.com/ebarsukov/gpt-telegram-assistant/releases)


<br/>

## Supported Docker tags

* `latest`: image with the latest version
* `candidate`: image with the release candidate version
* `x.y.z`: image with the specific release version
<br/>

<br/>

## Recommended GPT-Telegram-Asistant Usage

Here is a usage of GPT-Telegram-Asistant using docker-compose. 

```yaml
services:

  dobot-arm-connector:
    image: gpt-telegram-asystant:latest
    restart: unless-stopped
    volumes:
      - ./gpt-telegram-asystant:/gpt-telegram-asystant

    environment:
      TELEGRAM_BOT_TOKEN: xxxxxxxxxx:xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      BUFFER_MSG_LIFETIME_SEC: 180
      WORKDIR: ./gpt-telegram-asystant
      OPENAI_API_KEY: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
      OPENAI_API_MODEL: gpt-3.5-turbo-0301
      OPENAI_CHAT_LIFETIME_SEC: 1800
      OPENAI_TEMPERATURE: 0.5
      OPENAI_MAX_TOKENS: 100
      OPENAI_CHAT_USER_PRESET: ''
      OPENAI_CHAT_SYSTEM_PRESET: "You are an intellectual assistant, The name of your interlocutor is {user_name}"


```