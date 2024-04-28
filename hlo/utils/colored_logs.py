import logging

from colored import (  # type: ignore[import-untyped]
    Style,
    fore,
)


class ColoredLogFormatter(logging.Formatter):
    def format(self, record):
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt  # noqa: SLF001

        # Replace the original format with one customized by logging level
        # https://dslackw.gitlab.io/colored/tables/colors/
        self._style._fmt = {  # noqa: SLF001
            logging.DEBUG: fore("dark_gray") + format_orig + Style.reset,
            logging.INFO: format_orig,
            logging.WARNING: fore("dark_orange") + format_orig + Style.reset,
            logging.ERROR: fore("red") + format_orig + Style.reset,
            logging.CRITICAL: fore("red") + format_orig + Style.reset,
        }[record.levelno]

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig  # noqa: SLF001

        return result
