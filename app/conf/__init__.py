"""
conf
"""
import os
import sys
import shutil
from loguru import logger
from dynaconf import Dynaconf

MN = "[Config]"

AUTHOR_NAME = "Evgeny Barsukov"
AUTHOR_EMAIL = "mail@ebarsukov.com"

CONFIG_FILES = [
    "general.yaml",
]


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
WORKDIR = os.getenv("WORKDIR")


def _set_logger(cfg, logdir):
    """Configuring the logging module"""
    logger.remove()
    logger.add(sys.stdout, level="TRACE")
    logger.add(
        f"{logdir}/{cfg.log.FILE_NAME_FORMAT}",
        level=cfg.log.LEVEL,
        format=cfg.log.FORMAT,
        rotation=cfg.log.ROTATION,
        retention=cfg.log.RETETION,
        compression="zip",
    )


def _get_env_vars(cfg):
    """Get the environment variables"""

    list_vars = []
    for key in cfg.environment.keys():
        list_vars.append(str(key))

    for name in list_vars:
        env_var_val = os.getenv(name)
        if env_var_val:
            cfg.environment[name] = env_var_val
            logger.debug(f"{MN} Get environment variable: {name}")


def _check_local_files(path) -> None:
    """Checking local configuration files"""
    for name in CONFIG_FILES:
        filepath = f"{path}/{name}"
        if not os.path.exists(filepath):
            logger.error(f"{MN} File does not exists: {filepath}")
            sys.exit()


def _check_workdir_config(path) -> None:
    """Checking workdir config files"""
    if not os.path.exists(path):
        os.makedirs(path)

    for file in CONFIG_FILES:
        filepath = os.path.join(path, file)
        if not os.path.exists(filepath):
            shutil.copy(os.path.join(CURRENT_DIR, file), filepath)
            logger.info(f"{MN} Make config file: {filepath}")


def app_name() -> str:
    "Returns APP Name"
    with open(CURRENT_DIR + "/../name", encoding="UTF-8") as file:
        return file.read().strip()


def app_version() -> str:
    "Returns APP Version"
    with open(CURRENT_DIR + "/../version", encoding="UTF-8") as file:
        return file.read().strip()


def _make_config():
    """Loading project configuration"""
    logger.info(f"{app_name().upper()} Ver.{app_version()} starting...")

    if WORKDIR:
        logdir = WORKDIR + "/log"
        confdir = WORKDIR + "/config"
        logger.info(f"{MN} Workdir: {WORKDIR}")
        _check_workdir_config(confdir)
    else:
        logdir = os.getcwd() + "/log"
        confdir = CURRENT_DIR
        logger.info(f"{MN} Workdir: {os.getcwd()}")

    _check_local_files(CURRENT_DIR)

    cfg = Dynaconf(
        envvar_prefix="DYNACONF",
        root_path=confdir,
        settings_files=CONFIG_FILES,
        environments=True,
    )

    for name in CONFIG_FILES:
        logger.debug(f"{MN} Loaded config file: {confdir}/{name}")

    _get_env_vars(cfg)
    _set_logger(cfg, logdir)

    cfg.app_name = app_name()
    cfg.app_version = app_version()
    cfg.author_name = AUTHOR_NAME
    cfg.author_email = AUTHOR_EMAIL

    return cfg


conf = _make_config()
