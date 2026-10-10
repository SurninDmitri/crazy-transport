"""Сценарные (функциональные) тесты Driver (SPEC 5.2, TC_S_41…TC_S_48).

Все действия выполняются через публичный интерфейс ``Driver``; перед
проверкой состояния вызывается ``get_current_status()``.
"""

from errors import NotEnoughEnergyError, NotEnoughStrengthError
from tests.constants import (
    Location,
    Mass,
    Messages,
)
from tests.steps import Steps


class TestFunctionalScenarios(Steps):
    """Сквозные сценарии 41–48 (Given: name="Крот-1", mass_kg=200.0)."""

    # region =====Happy=====
    def test_s41_two_jumps_on_surface(self):
        """TC_S_41: два последовательных прыжка."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Обычный прыжок")
        self.when_basic_jump()

        self.step("Дальний прыжок")
        self.when_long_jump()

        # Assert

        self.step("Проверка статуса после двух прыжков")
        self.assert_status(expected={"distance": 40.0,
                                     "strength": 81.0,
                                     "reactor_energy": 100.0,
                                     "location_state": Location.SURFACE})  # fmt: skip

    def test_s42_two_reactor_jumps(self):
        """TC_S_42: два прыжка с форсажем."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Первый прыжок с форсажем")
        self.when_long_jump(use_reactor=True)

        self.step("Второй прыжок с форсажем")
        self.when_long_jump(use_reactor=True)

        # Assert

        self.step("Проверка статуса после двух форсажей")
        self.assert_status(expected={"distance": 90.0,
                                     "strength": 72.0,
                                     "reactor_energy": 0.0,
                                     "location_state": Location.SURFACE})  # fmt: skip

    def test_s45_full_underground_cycle(self):
        """TC_S_45: погружение, бурение и возврат."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Погружение под землю")
        self.when_go_underground()

        self.step("Подземное бурение")
        self.when_drill_forward()

        self.step("Возврат на поверхность")
        self.when_return_to_surface()

        # Assert

        self.step("Проверка статуса после полного цикла")
        self.assert_status(expected={"distance": 40.0,
                                     "strength": 72.0,
                                     "reactor_energy": 50.0,
                                     "location_state": Location.SURFACE})  # fmt: skip

    def test_s46_recovery_after_surface_jump(self):
        """TC_S_46: восстановление после пересечения 100 м на поверхности."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Погружение под землю")
        self.when_go_underground()

        self.step("Подземное бурение")
        self.when_drill_forward()

        self.step("Возврат на поверхность")
        self.when_return_to_surface()

        self.step("Дальний прыжок")
        self.when_long_jump()

        self.step("Обычный прыжок")
        self.when_basic_jump()

        # Assert

        self.step("Проверка статуса до отметки 100 м")
        self.assert_status(expected={"distance": 80.0,
                                     "strength": 53.0,
                                     "reactor_energy": 50.0,
                                     "location_state": Location.SURFACE})  # fmt: skip

        # Act

        self.step("Дальний прыжок после отметки 100 м")
        self.when_long_jump()

        # Assert

        self.step("Проверка восстановления силы и энергии")
        self.assert_status(expected={"distance": 110.0,
                                     "strength": 74.0,
                                     "reactor_energy": 85.0,
                                     "location_state": Location.SURFACE})  # fmt: skip

    def test_s47_recovery_after_underground_drill(self):
        """TC_S_47: восстановление после пересечения 100 м под землёй."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Погружение под землю")
        self.when_go_underground()

        self.step("Подземное бурение")
        self.when_drill_forward()

        self.step("Возврат на поверхность")
        self.when_return_to_surface()

        self.step("Обычный прыжок")
        self.when_basic_jump()

        self.step("Дальний прыжок")
        self.when_long_jump()

        self.step("Погружение под землю")
        self.when_go_underground()

        # Assert

        self.step("Проверка статуса до отметки 100 м")
        self.assert_status(expected={"distance": 80.0,
                                     "strength": 47.0,
                                     "reactor_energy": 50.0,
                                     "location_state": Location.UNDERGROUND})  # fmt: skip

        # Act

        self.step("Бурение после отметки 100 м")
        self.when_drill_forward()

        # Assert

        self.step("Проверка восстановления силы и энергии")
        self.assert_status(expected={"distance": 120.0,
                                     "strength": 66.0,
                                     "reactor_energy": 35.0,
                                     "location_state": Location.UNDERGROUND})  # fmt: skip

    def test_s48_crossing_100m_and_200m_marks(self):
        """TC_S_48: отметки 100 м (поверхность) и 200 м (под землёй)."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Прыжки до отметки 100 м")
        self.when_basic_jump()
        self.when_long_jump()
        self.when_long_jump()
        self.when_basic_jump()
        self.when_long_jump()
        self.when_long_jump()

        self.step("Дальний прыжок и погружение до отметки 200 м")
        self.when_long_jump()
        self.when_go_underground()
        self.when_drill_forward()

        # Assert

        self.step("Проверка пересечения отметок 100 и 200 м")
        self.assert_status(expected={"distance": 210.0,
                                     "strength": 68.0,
                                     "reactor_energy": 85.0,
                                     "location_state": Location.UNDERGROUND})  # fmt: skip
    # endregion

    # region =====Error=====
    def test_s43_third_reactor_jump_without_energy_raises(self):
        """TC_S_43: третий прыжок с реактором без энергии."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Два прыжка с форсажем")
        self.when_long_jump(use_reactor=True)
        self.when_long_jump(use_reactor=True)

        # Act + Assert

        self.step("Проверка ошибки при третьем форсаже без энергии")
        self.assert_raises_with_message(exception=NotEnoughEnergyError,
                                        message=Messages.NO_ENERGY_BOOST,
                                        action=self.when_long_jump,
                                        use_reactor=True)  # fmt: skip

    def test_s44_jump_with_exhausted_strength_raises(self):
        """TC_S_44: дальний прыжок при исчерпанной силе."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Исчерпание силы перемещениями")
        for _ in range(4):
            self.when_go_underground()
            self.when_return_to_surface()

        self.step("Три дальних прыжка")
        for _ in range(3):
            self.when_long_jump()

        # Assert

        self.step("Проверка остаточного статуса")
        self.assert_status(expected={"distance": 90.0,
                                     "strength": 10.0,
                                     "reactor_energy": 100.0,
                                     "location_state": Location.SURFACE})  # fmt: skip

        # Act + Assert

        self.step("Проверка ошибки при нехватке силы")
        self.assert_raises_with_message(exception=NotEnoughStrengthError,
                                        message=Messages.NO_STRENGTH_LONG,
                                        action=self.when_long_jump)  # fmt: skip
    # endregion