"""Иерархия исключений «Терра-Хоппер» (SPEC, раздел 6).

Ошибки параметров описаны стандартным ``ValueError`` и здесь не объявляются.
"""


class TerraHopperError(Exception):
    """Корень доменных исключений транспорта."""


class NoTransportError(TerraHopperError):
    """У водителя не выбран транспорт."""


class InvalidLocationError(TerraHopperError):
    """Действие недопустимо в текущей локации."""


class NotEnoughStrengthError(TerraHopperError):
    """Недостаточно силы для выполнения действия."""


class NotEnoughEnergyError(TerraHopperError):
    """Недостаточно энергии реактора для выполнения действия."""
