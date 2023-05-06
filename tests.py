import pytest
from storage_system import Inverter, BatteryModule, Controller, StorageSystem


@pytest.fixture
def inverter():
    return Inverter()


@pytest.fixture
def batteries():
    return [BatteryModule(100), BatteryModule(100)]


@pytest.fixture
def controller():
    return Controller()


@pytest.fixture
def storage_system():
    return StorageSystem(controller, inverter, batteries)


def test_initial(storage_system):
    storage_system.control(10, 10)
    assert storage_system.soc == 0
