from tests.fixtures import *


"""
1. There is more PV production than house demand, the power excess is first used to charge the storage system and then sent to the grid.
2. There here is more PV production than house demand, but the storage system is already fully charged, all the surplus energy is sent to the grid.
3. There is less PV production than house demand, the storage system supplies power to the house and the grid provides the remaining power.
4. There here is less PV production than house demand, but the storage system is already empty, the grid provides all the power to the house.
5. There here is equal PV production and house demand, the storage system remains at its current state and the grid provides the remaining power.
"""

def test_production_greater_than_demand(storage_system, pv_panel, house):
    storage_system.control(pv_panel, house)
    assert storage_system.soc == 0

def test_production_greater_than_demand_storage_full(storage_system, pv_panel, house):
    storage_system.control(pv_panel, house)
    assert storage_system.soc == 0

def test_production_less_than_demand(storage_system, pv_panel, house):
    storage_system.control(pv_panel, house)
    assert storage_system.soc == 0

def test_production_less_than_demand_storage_empty(storage_system, pv_panel, house):
    storage_system.control(pv_panel, house)
    assert storage_system.soc == 0

def test_production_equal_than_demand(storage_system, pv_panel, house):
    storage_system.control(pv_panel, house)
    assert storage_system.soc == 0
