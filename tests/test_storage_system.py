import pytest

from storage_system import Inverter, BatteryModule, Controller, StorageSystem


@pytest.fixture
def storage_system(request):
    num_battery_modules = request.param[0]
    battery_capacity = request.param[1]
    controller = Controller()
    inverter = Inverter()
    batteries = [BatteryModule(battery_capacity) for _ in range(num_battery_modules)]
    storage_system = StorageSystem(controller, inverter, batteries)
    yield storage_system


class TestStorageSystem:
    """
    1. There is more PV production than house demand, the power excess is first used to charge the storage system and then sent to the grid.
    2. There here is more PV production than house demand, but the storage system is already fully charged, all the power excess is sent to the grid.
    3. There is less PV production than house demand, the storage system supplies power to the house and the grid provides the remaining power.
    4. There here is less PV production than house demand, but the storage system is already empty, the grid provides all the power to the house.
    5. There here is equal PV production and house demand, the storage system remains at its current state and the grid provides the remaining power.
    """

    @pytest.mark.parametrize(
        "storage_system, production, power_demand, actual_soc, expected_soc, expected_power_to_house, "
        "expected_power_to_grid, expected_power_from_grid",
        [
            ([1, 100], 20, 10, 0, 10, 10, 0, 0),  # 1.
            ([1, 100], 20, 10, 100, 100, 10, 10, 0),  # 2.
            ([1, 100], 10, 20, 50, 40, 20, 0, 0),  # 3.
            ([1, 100], 10, 20, 0, 0, 10, 0, 10),  # 4.
            ([1, 100], 10, 10, 50, 50, 10, 0, 0),  # 5.
        ], indirect=['storage_system']
    )
    def test_storage_system(self, storage_system, production, power_demand, actual_soc, expected_soc,
                            expected_power_to_grid, expected_power_to_house, expected_power_from_grid):
        storage_system.soc = actual_soc
        storage_system.production = production
        storage_system.power_demand = power_demand
        storage_system.control()

        assert storage_system.soc == expected_soc
        assert storage_system.power_to_house == expected_power_to_house
        assert storage_system.power_to_grid == expected_power_to_grid
        assert storage_system.power_from_grid == expected_power_from_grid
