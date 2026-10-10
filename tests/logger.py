"""Логирование с поддержкой вложенности вызовов (SPEC)."""

import contextvars
import functools
import logging
import os
import sys
from datetime import datetime


_LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "tests",
    "logs"
)

os.makedirs(_LOG_DIR, exist_ok=True)

_log_file = os.path.join(_LOG_DIR, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

_file_handler = logging.FileHandler(_log_file, encoding="utf-8")
_file_handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s", datefmt="%H:%M:%S"))

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s", datefmt="%H:%M:%S"))

_logger = logging.getLogger("terra_hopper_tests")
_logger.setLevel(logging.INFO)
_logger.addHandler(_file_handler)
_logger.addHandler(_console_handler)
_logger.propagate = False


_call_depth = contextvars.ContextVar("_call_depth", default=0)
_current_test = contextvars.ContextVar("_current_test", default="")

_INDENT = "    "


def _get_depth() -> int:
    return _call_depth.get()


def _set_depth(depth: int):
    _call_depth.set(depth)


def begin_test(name: str) -> None:
    """Открывает лог теста: шапка с именем и сброс вложенности."""
    _set_depth(0)
    _current_test.set(name)
    _logger.info("=" * 70)
    _logger.info(f"TEST: {name}")
    _logger.info("=" * 70)


def end_test() -> None:
    """Закрывает лог теста пустой строкой-разделителем."""
    _logger.info("")
    _current_test.set("")


def step(message: str) -> None:
    """Логирует ручной шаг на текущем уровне вложенности."""
    indent = _INDENT * _get_depth()
    _logger.info(f"{indent}{message}")


def log_failure(message: str) -> None:
    """Логирует сообщение об ошибке проверки на текущем уровне вложенности."""
    indent = _INDENT * _get_depth()
    pad = indent + "   "
    lines = str(message).splitlines() or [""]
    _logger.info(f"{indent}\u2717 FAIL: {lines[0]}")
    for line in lines[1:]:
        _logger.info(f"{pad}{line}")


def logger(func):
    """Декоратор: логирует вход/выход метода с отступом по глубине вызова."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        depth = _get_depth()
        indent = _INDENT * depth
        qualname = f"{func.__module__}.{func.__qualname__}"

        _logger.info(f"{indent}\u2192 {qualname}")
        _set_depth(depth + 1)
        try:
            result = func(*args, **kwargs)
            _logger.info(f"{indent}\u2713 {qualname}")
            return result
        except Exception as e:
            label = type(e).__name__
            if not isinstance(e, AssertionError):
                text = str(e).strip()
                if text:
                    label = f"{label}: {text}"
            _logger.info(f"{indent}\u2717 {qualname} ({label})")
            raise
        finally:
            _set_depth(depth)
    return wrapper