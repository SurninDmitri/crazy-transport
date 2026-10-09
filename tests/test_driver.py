"""Модульные тесты Driver (SPEC 5.1, TC_P_14…TC_P_20, TC_N_39…TC_N_40)."""

from errors import NoTransportError
from terra_hopper import TerraHopper
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
        driver = self.given_driver()

        # Act
        attached = driver.terra_hopper

        # Assert
        self.assertIsNone(obj=attached)
    # endregion


class TestCreateHopper(Steps):
    """create_hopper (SPEC 4.3.1)."""

    # region =====Happy=====
    def test_p15_create_hopper_with_defaults(self):
        """TC_P_15: создание транспорта с параметрами по умолчанию."""
        # Arrange
        driver = self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act
        hopper = driver.terra_hopper

        # Assert
        self.assertIsInstance(obj=hopper,
                              cls=TerraHopper,
                              msg=None)  # fmt: skip
        self.assertEqual(first=hopper.name,
                         second=Transport.NAME,
                         msg=None)  # fmt: skip
        self.assert_that(actual=hopper.mass_kg,
                         expected=Mass.DEFAULT,
                         msg=None)  # fmt: skip
        self.assert_status(expected={"distance": Distance.DEFAULT,
                                     "strength": Strength.MAX,
                                     "reactor_energy": ReactorEnergy.MAX,
                                     "location_state": Location.SURFACE})  # fmt: skip

    def test_p16_create_hopper_with_all_parameters(self):
        """TC_P_16: создание транспорта со всеми параметрами."""
        # Arrange
        driver = self.given_driver_with_hopper(mass_kg=350.0,
                                               strength=80.0,
                                               reactor_energy=60.0)  # fmt: skip

        # Act
        hopper = driver.terra_hopper

        # Assert
        self.assert_that(actual=hopper.mass_kg,
                         expected=350.0,
                         msg=None)  # fmt: skip
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
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act
        before = self.current_status()
        self.when_basic_jump()

        # Assert
        expected = self.expected_after_basic_jump(mass_kg=Mass.DEFAULT,
                                                  status=before)  # fmt: skip
        self.assert_status(expected=expected)

    def test_p18_long_jump_with_reactor_delegated(self):
        """TC_P_18: дальний прыжок с форсажем выполняется через водителя."""
        # Arrange
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT)

        # Act
        before = self.current_status()
        self.when_long_jump(use_reactor=True)

        # Assert
        expected = self.expected_after_long_jump(mass_kg=Mass.DEFAULT,
                                                 status=before,
                                                 use_reactor=True)  # fmt: skip
        self.assert_status(expected=expected)

    def test_p19_drill_forward_delegated(self):
        """TC_P_19: подземное бурение выполняется через водителя."""
        # Arrange
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT,
                                      location_state=Location.UNDERGROUND)  # fmt: skip

        # Act
        before = self.current_status()
        self.when_drill_forward()

        # Assert
        expected = self.expected_after_drill_forward(mass_kg=Mass.DEFAULT,
                                                     status=before)  # fmt: skip
        self.assert_status(expected=expected)
    # endregion

    # region =====Error=====
    def test_n39_actions_without_transport_raise(self):
        """TC_N_39: любое действие без транспорта вызывает ошибку."""
        # Arrange
        self.given_no_transport()
        actions = (
            self.when_basic_jump,
            self.when_long_jump,
            self.when_go_underground,
            self.when_return_to_surface,
            self.when_drill_forward,
        )

        # Act + Assert
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
        self.given_driver_with_hopper(mass_kg=Mass.DEFAULT,
                                      strength=80.0,
                                      reactor_energy=90.0,
                                      distance=20.0,
                                      location_state=Location.SURFACE)  # fmt: skip

        # Act
        status = self.current_status()

        # Assert
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
        self.given_no_transport()

        # Act + Assert
        self.assert_raises_with_message(exception=NoTransportError,
                                        message=Messages.NO_TRANSPORT,
                                        action=self.current_status)  # fmt: skip
    # endregion