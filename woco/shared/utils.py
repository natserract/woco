import logging
import logging.config
from typing import (
    Optional,
    Text,
)
import woco.config as cfg

def configure_logging(
    log_level: Optional[int] = None,
) -> None:
    _log_level = log_level
    if _log_level is None:
        _log_level = logging.getLevelName(cfg.DEFAULT_LOG_LEVEL)

    logging.getLogger(__name__).setLevel(_log_level)
