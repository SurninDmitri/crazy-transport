"""Класс TerraHopper — публичный интерфейс (SPEC, раздел 3).

Заглушка: описаны только сигнатуры. Реализацию пишет разработчик.
"""


class TerraHopper:
    """Земляной Кенгуру-Крот «Терра-Хоппер»."""

    def __init__(
        self,
        name: str,
        mass_kg: float,
        strength: float = 100.0,
        reactor_energy: float = 100.0,
    ) -> None:
        pass

    def basic_jump(self) -> None:
        pass

    def long_jump(self, use_reactor: bool = False) -> None:
        pass

    def _apply_distance_recovery(self) -> None:
        pass

    def get_current_status(self) -> dict:
        pass

    def go_underground(self) -> None:
        pass

    def return_to_surface(self) -> None:
        pass

    def drill_forward(self) -> None:
        pass
