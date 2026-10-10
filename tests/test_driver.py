"""Модульные тесты Driver (SPEC 5.1, TC_P_14…TC_P_20, TC_N_39…TC_N_40)."""

from terra_hopper import NoTransportError, TerraHopper
from tests.constants import (
    Distance,
    Location,
    Mass,
    Messages,
    ReactorEnergy,
    Strength,
    Transport,
)
from tests.steps import Steps


class TestDriverInit(Steps):
    """Конструктор Driver (SPEC 4.2)."""

    # region =====Happy=====
    def test_p14_init_without_transport(self):
        """TC_P_14: водитель без транспорта."""
        # Arrange

        self.step("Создание водителя без транспорта")
        driver = self.given_driver()

        # Act

        self.step("Получение привязанного транспорта")
        attached = driver.terra_hopper

        # Assert

        self.step("Проверка отсутствия транспорта")
        self.assertIsNone(obj=attached)
    # endregion


class TestCreateHopper(Steps):
    """create_hopper (SPEC 4.3.1)."""

# region =====Happy=====
    def test_p15_create_hopper_with_defaults(self):
        """TC_P_15: создание транспорта с параметрами по умолчанию."""
        # Arrange

        self.step("Создание водителя и транспорта с параметрами по умолчанию")
        driver = self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Получение созданного транспорта")
        hopper = driver.terra_hopper

        # Assert

        self.step("Проверка типа транспорта (TerraHopper)")
        self.assertIsInstance(obj=hopper,
                              cls=TerraHopper,
                              msg=None)  # fmt: skip

        self.step("Проверка имени транспорта")
        self.assertEqual(first=hopper.name,
                         second=Transport.NAME,
                         msg=None)  # fmt: skip

        self.step("Проверка массы транспорта")
        self.assert_that(actual=hopper.mass_kg,
                         expected=Mass.DEFAULT,
                         msg=None)  # fmt: skip

        self.step("Проверка статуса: distance, strength, reactor_energy, location_state")
        self.assert_status(expected={"distance": Distance.DEFAULT,
                                      "strength": Strength.MAX,
                                      "reactor_energy": ReactorEnergy.MAX,
                                      "location_state": Location.SURFACE})  # fmt: skip

    def test_p16_create_hopper_with_all_parameters(self):
        """TC_P_16: создание транспорта со всеми параметрами."""
        # Arrange

        self.step("Создание водителя и транспорта со всеми параметрами")
        driver = self.given_driver_with_hopper(mass_kg=350.0,
                                               strength=80.0,
                                               reactor_energy=60.0)  # fmt: skip

        # Act

        self.step("Получение созданного транспорта")
        hopper = driver.terra_hopper

        # Assert

        self.step("Проверка массы транспорта")
        self.assert_that(actual=hopper.mass_kg,
                         expected=350.0,
                         msg=None)  # fmt: skip

        self.step("Проверка статуса")
        self.assert_status(expected={"distance": Distance.DEFAULT,
                                     "strength": 80.0,
                                     "reactor_energy": 60.0,
                                     "location_state": Location.SURFACE})  # fmt: skip
    # endregion


class TestDriverActions(Steps):
    """Делегирование действий транспорту (SPEC 4.3.2)."""

    # region =====Happy=====
    def test_p17_basic_jump_delegated(self):
        """TC_P_17: обычный прыжок выполняется через водителя."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Снятие статуса до прыжка")
        before = self.current_status()

        self.step("Обычный прыжок")
        self.when_basic_jump()

        # Assert

        self.step("Проверка статуса после прыжка")
        expected = self.expected_after_basic_jump(mass_kg=Mass.DEFAULT,
                                                  status=before)  # fmt: skip
        self.assert_status(expected=expected)

    def test_p18_long_jump_with_reactor_delegated(self):
        """TC_P_18: дальний прыжок с форсажем выполняется через водителя."""
        # Arrange

        self.step("Создание водителя с транспортом")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act

        self.step("Снятие статуса до прыжка")
        before = self.current_status()

        self.step("Дальний прыжок с форсажем")
        self.when_long_jump(use_reactor=True)

        # Assert

        self.step("Проверка уменьшения силы и энергии, роста дистанции")
        expected = self.expected_after_long_jump(mass_kg=Mass.DEFAULT,
                                                 status=before,
                                                 use_reactor=True)  # fmt: skip
        self.assert_status(expected=expected)

    def test_p19_drill_forward_delegated(self):
        """TC_P_19: подземное бурение выполняется через водителя."""
        # Arrange

        self.step("Создание водителя с транспортом под землёй")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT,
                                      location_state=Location.UNDERGROUND)  # fmt: skip

        # Act

        self.step("Снятие статуса до бурения")
        before = self.current_status()

        self.step("Подземное бурение")
        self.when_drill_forward()

        # Assert

        self.step("Проверка статуса после бурения")
        expected = self.expected_after_drill_forward(mass_kg=Mass.DEFAULT,
                                                     status=before)  # fmt: skip
        self.assert_status(expected=expected)
    # endregion

    # region =====Error=====
    def test_n39_actions_without_transport_raise(self):
        """TC_N_39: любое действие без транспорта вызывает ошибку."""
        # Arrange

        self.step("Создание водителя без транспорта")
        self.given_no_transport()
        actions = (
            self.when_basic_jump,
            self.when_long_jump,
            self.when_go_underground,
            self.when_return_to_surface,
            self.when_drill_forward,
        )

        # Act + Assert

        self.step("Проверка ошибки для каждого действия без транспорта")
        for action in actions:
            with self.subTest(action=action.__name__):
                self.assert_raises_with_message(exception=NoTransportError,
                                                message=Messages.NO_TRANSPORT,
                                                action=action)  # fmt: skip
    # endregion


class TestDriverStatus(Steps):
    """Делегирование get_current_status (SPEC 4.3.3)."""

    # region =====Happy=====
    def test_p20_get_current_status_delegated(self):
        """TC_P_20: текущий статус получается через водителя."""
        # Arrange

        self.step("Создание водителя с заданными параметрами")
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT,
                                      strength=80.0,
                                      reactor_energy=90.0,
                                      distance=20.0,
                                      location_state=Location.SURFACE)  # fmt: skip

        # Act

        self.step("Получение текущего статуса")
        status = self.current_status()

        # Assert

        self.step("Проверка статуса")
        self.assert_that(actual=status,
                         expected={"distance": 20.0,
                                   "strength": 80.0,
                                   "reactor_energy": 90.0,
                                   "location_state": Location.SURFACE})  # fmt: skip
    # endregion

    # region =====Error=====
    def test_n40_get_current_status_without_transport_raises(self):
        """TC_N_40: Нельзя получить текущий статус без активного транспорта."""
        # Arrange

        self.step("Создание водителя без транспорта")
        self.given_no_transport()

        # Act + Assert

        self.step("Проверка ошибки при запросе статуса без транспорта")
        self.assert_raises_with_message(exception=NoTransportError,
                                        message=Messages.NO_TRANSPORT,
                                        action=self.current_status)  # fmt: skip
    # endregion