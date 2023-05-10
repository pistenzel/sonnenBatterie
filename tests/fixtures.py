"""
Common fixture that can be used in different test cases
"""

import pytest

from storage_system import Inverter, BatteryModule, Controller, StorageSystem


@pytest.fixture
def inverter():
    return Inverter()


@pytest.fixture
def batteries():
    return [BatteryModule(100, 30), BatteryModule(100, 0)]


@pytest.fixture
def controller():
    return Controller()


@pytest.fixture
def storage_system(request):
    num_inverter = request.param[0]  # Not used at the moment as all systems have only 1
    num_controller = request.param[1]  # Not used at the moment as all systems have only 1
    num_battery_modules = request.param[2]
    battery_capacity = request.param[3]
    batteries = [BatteryModule(battery_capacity) for _ in range(num_battery_modules)]
    storage_system = StorageSystem(controller, inverter, batteries)
    yield storage_system
    del storage_system

