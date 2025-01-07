import logging
from enum import StrEnum


class ConsoleFormat(StrEnum):
    RESET = "\033[0m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    HIGHLIHT_BLACK = "\033[40m"
    HIGHLIGHT_RED = "\033[41m"
    HIGHLIGHT_GREEN = "\033[42m"
    HIGHLIGHT_YELLOW = "\033[43m"
    HIGHLIGHT_BLUE = "\033[44m"
    HIGHLIGHT_MAGENTA = "\033[45m"
    HIGHLIGHT_CYAN = "\033[46m"
    HIGHLIGHT_WHITE = "\033[47m"

    BOLD = "\033[1m"
    LIGHT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    HIGHLIGHT = "\033[7m"
    STRIKETHROUGH = "\033[9m"


class ConsoleFormatter(logging.Formatter):
    fmt = "{asctime} - {name} - {levelname} - {message}"
    style = "{"
    validate = True

    COLOURS = {
        logging.DEBUG: ConsoleFormat.WHITE,
        logging.INFO: ConsoleFormat.BLUE,
        logging.WARNING: ConsoleFormat.YELLOW,
        logging.ERROR: ConsoleFormat.RED,
        logging.CRITICAL: ConsoleFormat.BOLD
        + ConsoleFormat.HIGHLIGHT_RED
        + ConsoleFormat.BLACK,
    }

    def _formatted_message(self, record: logging.LogRecord) -> str:
        log_colour = self.COLOURS.get(record.levelno, ConsoleFormat.RESET)
        return f"{log_colour}{self.fmt}{ConsoleFormat.RESET}"

    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(
            fmt=self._formatted_message(record=record),
            style=self.style,  # type: ignore[arg-type]
            validate=self.validate,
        )
        return formatter.format(record)


_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(logging.DEBUG)

LOGGER = logging.getLogger("motogp-analytics")
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(_stream_handler)
