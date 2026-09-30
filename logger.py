import logging


def get_logger(name="codesentinel"):
    """Return a logger that writes events to codesentinel.log."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("codesentinel.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(handler)
    return logger