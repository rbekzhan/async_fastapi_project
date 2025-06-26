import logging

logger = logging.getLogger("app_logger")

def setup_logger(level: str = "INFO"):
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )