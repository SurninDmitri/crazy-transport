"""Класс Driver — менеджер транспорта (SPEC, раздел 4).

Заглушка: описаны только сигнатуры. Реализацию пишет разработчик.
"""


class Driver:
    """Контроллер-менеджер, управляющий транспортом."""

    def __init__(self) -> None:
        pass

    def create_hopper(
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

    def go_underground(self) -> None:
        pass

    def return_to_surface(self) -> None:
        pass

    def drill_forward(self) -> None:
        pass

    def get_current_status(self) -> dict:
        pass
