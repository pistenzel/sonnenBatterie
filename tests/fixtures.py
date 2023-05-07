
import pytest
from storage_system import Inverter, BatteryModule, Controller, StorageSystem


@pytest.fixture
def pv_panel():
    return {
        'power': 10,
        'voltage': 10,
        'current': 10
    }


@pytest.fixture
def house():
    return {
        'power': 10,
        'voltage': 10,
        'current': 10,
        'frequency': 10
    }


@pytest.fixture
def grid():
    return {
        'power': 10,
        'voltage': 10,
        'frequency': 10
    }


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
def storage_system(controller, inverter, batteries):
    return StorageSystem(controller, inverter, batteries)

