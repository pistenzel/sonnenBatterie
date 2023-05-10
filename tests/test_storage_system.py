import pytest

from tests.fixtures import storage_system


class TestStorageSystem:
    """
    1. There is more PV production than house demand, the power excess is first used to charge the storage system and
       then sent to the grid.
    2. There here is more PV production than house demand, but the storage system is already fully charged, all the
       power excess is sent to the grid.
    3. There is less PV production than house demand, the storage system supplies power to the house and the grid
       provides the remaining power.
    4. There here is less PV production than house demand, but the storage system is already empty, the grid provides
       all the power to the house.
    5. There here is equal PV production and house demand, the storage system remains at its current state and the grid
       provides the remaining power.
    """

    @pytest.mark.parametrize(
        "storage_system, production, power_demand, soc, expected_soc, expected_power_to_house, "
        "expected_power_to_grid, expected_power_from_grid",
        [
            ([1, 1, 1, 100], 20, 10, 0, 10, 10, 0, 0),  # 1. / Basic
            ([1, 1, 1, 100], 20, 10, 100, 100, 10, 10, 0),  # 2.  / Basic
            ([1, 1, 1, 100], 10, 20, 50, 40, 20, 0, 0),  # 3.  / Basic
            ([1, 1, 1, 100], 10, 20, 0, 0, 10, 0, 10),  # 4.  / Basic
            ([1, 1, 1, 100], 10, 10, 50, 50, 10, 0, 0),  # 5.  / Basic

            ([1, 1, 3, 100], 20, 10, 0, 10, 10, 0, 0),  # 1. / Standard
            ([1, 1, 3, 100], 20, 10, 300, 300, 10, 10, 0),  # 2.  / Standard
            ([1, 1, 3, 100], 10, 20, 150, 140, 20, 0, 0),  # 3.  / Standard
            ([1, 1, 3, 100], 10, 20, 0, 0, 10, 0, 10),  # 4.  / Standard
            ([1, 1, 3, 100], 10, 10, 150, 150, 10, 0, 0),  # 5.  / Standard

            ([1, 1, 5, 100], 20, 10, 0, 10, 10, 0, 0),  # 1. / Pro
            ([1, 1, 5, 100], 20, 10, 500, 500, 10, 10, 0),  # 2.  / Pro
            ([1, 1, 5, 100], 10, 20, 250, 240, 20, 0, 0),  # 3.  / Pro
            ([1, 1, 5, 100], 10, 20, 0, 0, 10, 0, 10),  # 4.  / Pro
            ([1, 1, 5, 100], 10, 10, 250, 250, 10, 0, 0),  # 5.  / Pro
        ], indirect=['storage_system']
    )
    def test_storage_system(self, storage_system, production, power_demand, soc, expected_soc,
                            expected_power_to_grid, expected_power_to_house, expected_power_from_grid):
        # Set the input values and initial state
        storage_system.set("soc", soc)
        storage_system.set("production", production)
        storage_system.set("power_demand", power_demand)

        # Run the control algorithm taking into account the current system status
        storage_system.control()

        # Check the controller result against expected results
        assert storage_system.get("soc") == expected_soc
        assert storage_system.get("power_to_house") == expected_power_to_house
        assert storage_system.get("power_to_grid") == expected_power_to_grid
        assert storage_system.get("power_from_grid") == expected_power_from_grid
