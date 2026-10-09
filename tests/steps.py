"""Шаги тестирования «Терра-Хоппер».

Класс ``Steps`` содержит подготовку (Given), действия (When), снятие состояния,
оракул расчёта ожидаемых значений и проверки (Assert).

Вызовы методов оформлены только именованными аргументами и защищены
``# fmt: skip`` от автоформатирования.
"""

import unittest

from tests.constants import (
    Distance,
    Formula,
    Location,
    Mass,
    ReactorEnergy,
    Strength,
    TOLERANCE,
    Transport,
)
from driver import Driver
from terra_hopper import TerraHopper


class Steps(unittest.TestCase):
    """Базовый класс тестов: данные, действия, оракул и проверки."""

    hopper = None
    driver = None

    # region =====Подготовка=====
    def given_hopper(
        self,
        name: str = Transport.NAME,
        mass_kg: float = Mass.DEFAULT,
        strength: float = None,
        reactor_energy: float = None,
        location_state: str = None,
        distance: float = None,
    ) -> TerraHopper:
        """Создаёт транспорт с указанными параметрами."""
        kwargs = {}
        if strength is not None:
            kwargs["strength"] = strength
        if reactor_energy is not None:
            kwargs["reactor_energy"] = reactor_energy
        self.hopper = TerraHopper(name=name,
                                  mass_kg=mass_kg,
                                  **kwargs)  # fmt: skip
        self._set_initial_state(hopper=self.hopper,
                                location_state=location_state,
                                distance=distance)  # fmt: skip
        return self.hopper

    def given_driver(self) -> Driver:
        """Создаёт водителя без транспорта."""
        self.driver = Driver()
        return self.driver

    def given_driver_with_hopper(
        self,
        name: str = Transport.NAME,
        mass_kg: float = Mass.DEFAULT,
        strength: float = None,
        reactor_energy: float = None,
        location_state: str = None,
        distance: float = None,
    ) -> Driver:
        """Создаёт водителя и привязывает к нему транспорт."""
        self.driver = Driver()
        kwargs = {}
        if strength is not None:
            kwargs["strength"] = strength
        if reactor_energy is not None:
            kwargs["reactor_energy"] = reactor_energy
        self.driver.create_hopper(name=name,
                                  mass_kg=mass_kg,
                                  **kwargs)  # fmt: skip
        self._set_initial_state(hopper=self.driver.terra_hopper,
                                location_state=location_state,
                                distance=distance)  # fmt: skip
        return self.driver

    def given_no_transport(self) -> Driver:
        """Водитель без транспорта (для проверки NoTransportError)."""
        return self.given_driver()
    # endregion

    # region =====Действия=====
    def when_basic_jump(self):
        return self._subject().basic_jump()

    def when_long_jump(self, use_reactor: bool = False):
        return self._subject().long_jump(use_reactor=use_reactor)  # fmt: skip

    def when_go_underground(self):
        return self._subject().go_underground()

    def when_return_to_surface(self):
        return self._subject().return_to_surface()

    def when_drill_forward(self):
        return self._subject().drill_forward()

    def when_apply_recovery(self):
        return self._hopper()._apply_distance_recovery()
    # endregion

    # region =====Снятие состояния=====
    def current_status(self) -> dict:
        return self._subject().get_current_status()
    # endregion

    # region =====Оракул=====
    @staticmethod
    def basic_jump_cost(mass_kg: float) -> float:
        return Formula.BASIC_JUMP_BASE + mass_kg / Formula.MASS_DIV

    @staticmethod
    def long_jump_cost(mass_kg: float) -> float:
        return Formula.LONG_JUMP_BASE + (mass_kg / Formula.MASS_DIV) * Formula.LONG_JUMP_FACTOR

    @staticmethod
    def drill_cost(mass_kg: float) -> float:
        return Formula.DRILL_BASE + (mass_kg / Formula.MASS_DIV) * Formula.DRILL_FACTOR

    @staticmethod
    def move_cost(mass_kg: float) -> float:
        return Formula.MOVE_BASE * (mass_kg / Formula.MASS_DIV)

    @staticmethod
    def recovery_amount(mass_kg: float) -> float:
        return Formula.RECOVERY_BASE - (mass_kg / Formula.RECOVERY_MASS_DIV) * Formula.RECOVERY_FACTOR

    @classmethod
    def expected_after_basic_jump(cls, mass_kg: float, status: dict) -> dict:
        cost = cls.basic_jump_cost(mass_kg=mass_kg)  # fmt: skip
        return {
            "distance": status["distance"] + Distance.BASIC_JUMP,
            "strength": status["strength"] - cost,
            "reactor_energy": status["reactor_energy"],
            "location_state": Location.SURFACE,
        }  # fmt: skip

    @classmethod
    def expected_after_long_jump(
        cls, mass_kg: float, status: dict, use_reactor: bool = False
    ) -> dict:
        cost = cls.long_jump_cost(mass_kg=mass_kg)  # fmt: skip
        if use_reactor:
            distance = status["distance"] + Distance.REACTOR_LONG_JUMP
            energy = status["reactor_energy"] - ReactorEnergy.CONSUMPTION
        else:
            distance = status["distance"] + Distance.LONG_JUMP
            energy = status["reactor_energy"]
        return {
            "distance": distance,
            "strength": status["strength"] - cost,
            "reactor_energy": energy,
            "location_state": Location.SURFACE,
        }  # fmt: skip

    @classmethod
    def expected_after_go_underground(cls, mass_kg: float, status: dict) -> dict:
        cost = cls.move_cost(mass_kg=mass_kg)  # fmt: skip
        return {
            "distance": status["distance"],
            "strength": status["strength"] - cost,
            "reactor_energy": status["reactor_energy"],
            "location_state": Location.UNDERGROUND,
        }  # fmt: skip

    @classmethod
    def expected_after_return_to_surface(cls, mass_kg: float, status: dict) -> dict:
        cost = cls.move_cost(mass_kg=mass_kg)  # fmt: skip
        return {
            "distance": status["distance"],
            "strength": status["strength"] - cost,
            "reactor_energy": status["reactor_energy"],
            "location_state": Location.SURFACE,
        }  # fmt: skip

    @classmethod
    def expected_after_drill_forward(cls, mass_kg: float, status: dict) -> dict:
        cost = cls.drill_cost(mass_kg=mass_kg)  # fmt: skip
        return {
            "distance": status["distance"] + Distance.DRILL,
            "strength": status["strength"] - cost,
            "reactor_energy": status["reactor_energy"] - ReactorEnergy.CONSUMPTION,
            "location_state": Location.UNDERGROUND,
        }  # fmt: skip

    @classmethod
    def expected_after_recovery(cls, mass_kg: float, status: dict) -> dict:
        gain = cls.recovery_amount(mass_kg=mass_kg)  # fmt: skip
        strength = min(status["strength"] + gain, Strength.MAX)  # fmt: skip
        reactor_energy = min(status["reactor_energy"] + gain, ReactorEnergy.MAX)  # fmt: skip
        return {
            "distance": status["distance"],
            "strength": strength,
            "reactor_energy": reactor_energy,
            "location_state": status["location_state"],
        }  # fmt: skip
    # endregion

    # region =====Проверки=====
    def assert_that(self, actual, expected, msg=None):
        """Сравнивает фактическое значение с ожидаемым."""
        if isinstance(expected, dict):  # fmt: skip
            self.assertIsInstance(obj=actual,
                                  cls=dict,
                                  msg=msg)  # fmt: skip
            for key, value in expected.items():
                self.assertIn(member=key,
                              container=actual,
                              msg=msg)  # fmt: skip
                value_msg = self._join_msg(prefix=key,
                                           msg=msg)  # fmt: skip
                self._assert_value(actual=actual[key],
                                   expected=value,
                                   msg=value_msg)  # fmt: skip
        else:
            self._assert_value(actual=actual,
                               expected=expected,
                               msg=msg)  # fmt: skip

    def assert_status(self, expected: dict, msg=None):
        """Сверяет результат get_current_status() с ожидаемым словарём."""
        if not msg:
            msg = "Текущий статус отличается от ожидаемого!"
        actual = self.current_status()
        self.assert_that(actual=actual,
                         expected=expected,
                         msg=msg)  # fmt: skip

    def _formatMessage(self, msg, standard_msg):
        """Сообщение об ошибке: сначала пояснение, затем оригинальный текст unittest."""
        if msg is None:
            return standard_msg
        return f"{msg}\n{standard_msg}"

    def assert_raises_with_message(self, exception, message, action, *args, **kwargs):
        """Проверяет тип исключения и его текст при выполнении действия."""
        with self.assertRaises(expected_exception=exception) as ctx:  # fmt: skip
            action(*args, **kwargs)  # fmt: skip
        error_message = str(object=ctx.exception)  # fmt: skip
        self.assertEqual(first=error_message,
                         second=message,
                         msg=None)  # fmt: skip
    # endregion

    # region =====Внутреннее=====
    @staticmethod
    def _set_initial_state(hopper, location_state=None, distance=None):
        """Задаёт начальные location_state/distance после создания."""
        if location_state:
            hopper.location_state = location_state
        if distance:
            hopper.distance = distance

    def _subject(self):
        """Объект, к которому применяются действия: водитель или транспорт."""
        return self.driver if self.driver else self.hopper

    def _hopper(self) -> TerraHopper:
        """Транспорт: явный или привязанный к водителю."""
        if self.hopper:
            return self.hopper
        return self.driver.terra_hopper

    def _assert_value(self, actual, expected, msg=None):
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):  # fmt: skip
            if abs(actual - expected) <= TOLERANCE:
                return
            standard_message = f"{actual} != {expected}"  # fmt: skip
            self.fail(self._formatMessage(msg=msg,
                                          standard_msg=standard_message))  # fmt: skip
        else:
            self.assertEqual(first=actual,
                             second=expected,
                             msg=msg)  # fmt: skip

    @staticmethod
    def _join_msg(prefix, msg):
        return prefix if msg is None else f"{prefix}: {msg}"
    # endregion
