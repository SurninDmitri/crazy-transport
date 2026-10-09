"""Константы и тестовые данные «Терра-Хоппер» (SPEC.md)."""

TOLERANCE = 1e-9


class Transport:
    NAME = "Крот-1"


class Mass:
    MIN = 100.0
    MAX = 500.0
    DEFAULT = 200.0


class Strength:
    MIN = 0.0
    MAX = 100.0
    DEFAULT = 100.0


class ReactorEnergy:
    MIN = 0.0
    MAX = 100.0
    DEFAULT = 100.0
    MIN_FOR_ACTION = 50.0
    CONSUMPTION = 50.0


class Distance:
    DEFAULT = 0.0
    BASIC_JUMP = 10.0
    LONG_JUMP = 30.0
    REACTOR_LONG_JUMP = 45.0
    DRILL = 40.0
    MARK = 100.0


class Location:
    SURFACE = "surface"
    UNDERGROUND = "underground"


class Formula:
    BASIC_JUMP_BASE = 3.0
    LONG_JUMP_BASE = 10.0
    DRILL_BASE = 10.0
    MOVE_BASE = 3.0
    MASS_DIV = 100.0
    LONG_JUMP_FACTOR = 2.0
    DRILL_FACTOR = 3.0
    RECOVERY_BASE = 45.0
    RECOVERY_MASS_DIV = 10.0
    RECOVERY_FACTOR = 0.5


class Messages:
    EMPTY_NAME = "Имя не может быть пустым."
    MASS_RANGE = "Масса должна быть в диапазоне 100.0…500.0 кг."
    STRENGTH_RANGE = "Сила должна быть в диапазоне 0…100."
    ENERGY_RANGE = "Энергия реактора должна быть в диапазоне 0…100."
    NO_TRANSPORT = "Транспорт не выбран. Сначала создайте транспорт!"
    JUMP_UNDERGROUND = "Прыжок невозможен: транспорт находится под землей."
    LONG_JUMP_UNDERGROUND = "Дальний прыжок невозможен: транспорт находится под землей."
    ALREADY_UNDERGROUND = "Транспорт уже находится под землей."
    ALREADY_SURFACE = "Транспорт уже находится на поверхности."
    DRILL_ON_SURFACE = "Подземное бурение невозможно на поверхности. Сначала погрузитесь."
    NO_STRENGTH_BASIC = "Не достаточно силы для выполнения обычного прыжка."
    NO_STRENGTH_LONG = "Недостаточно силы для выполнения дальнего прыжка."
    NO_STRENGTH_DIVE = "Недостаточно силы для погружения под землю."
    NO_STRENGTH_RETURN = "Недостаточно силы для возвращения на поверхность."
    NO_STRENGTH_DRILL = "Недостаточно силы для подземного бурения."
    NO_ENERGY_BOOST = "Недостаточно энергии реактора для форсажа (требуется 50.0)."
    NO_ENERGY_DRILL = "Недостаточно энергии реактора для запуска буров (требуется 50.0)."
