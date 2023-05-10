from abc import ABC


class Controller:
    """
    EM controller: handles the energy logic and issues all necessary commands to each of the devices
    """
    def __init__(self):
        pass

    def control(self, production, consumption):
        pass


class Inverter:
    """
    Inverter: device inside the sonnenBattery in charge of controlling the power flow to the batteries.
    Available values to read are:
    - Maximum power that the inverter can charge/discharge in Watts
    - Battery voltage in Volts
    - Battery current that is flowing to/from inverter in Amps
    - Power inverter is releasing/storing in the batteries in Watts
        - positive value notates inverter power is flowing into the batteries (charging)
        - negative value notates battery power is flowing into the inverter (discharging)
    - Inverter sensed grid frequency in Hertz
    - Inverter sensed grid Voltage in Volts
    """
    def __init__(self):
        self.max_power: float = 0
        self.voltage: float = 0
        self.current: float = 0
        self.power: float = 0
        self.grid_frequency: float = 0
        self.grid_voltage: float = 0


class BatteryModule:
    """
    Battery module (BMS): each of the battery packs that can be connected into a sonnenBatterie storage system.
    Values available to be read from each of them are:
    - Module temperature in Celsius degrees
    - Module voltage in Volts.
    - Maximum power that the battery module can charge or discharge in Watts.
    """
    def __init__(self, capacity, soc=0):
        self.capacity: float = capacity
        self.soc: float = soc
        self.temperature: float = 0
        self.voltage: float = 0
        self.max_power: float = 0


class BaseStorageSystem(ABC):
    """
    sonnenBatterie base storage system. It can release energy from the battery modules into the house grid or store energy
    from the house grid into the battery modules. Available configurations and values are:
    - Power command in Watts. Commands can be:
        - charge: positive Watts value
        - discharge: negative Watts value
    - Any value available from any of the internal components (inverter and battery modules)
    """
    def __init__(self, controller, inverter, batteries):
        self.controller: Controller = controller
        self.inverter: Inverter = inverter
        self.batteries: list[BatteryModule] = batteries
        self.capacity: float = sum(b.capacity for b in self.batteries)
        self.soc: float = 0
        self.production: float = 0
        self.power_demand: float = 0
        self.power_to_grid: float = 0
        self.power_to_house: float = 0
        self.power_from_grid: float = 0

    def set(self, key: str, value: float) -> bool:
        self.__setattr__(key, value)
        return True

    def get(self, key: str) -> float:
        return self.__getattribute__(key)

    def control(self, **kwargs):
        raise NotImplemented

    def charge(self, power):
        raise NotImplemented

    def discharge(self, power):
        raise NotImplemented


class StorageSystem(BaseStorageSystem):
    """
    sonnenBatterie storage system. It can release energy from the battery modules into the house grid or store energy
    from the house grid into the battery modules. Available configurations and values are:
    - Power command in Watts. Commands can be:
        - charge: positive Watts value
        - discharge: negative Watts value
    - Any value available from any of the internal components (inverter and battery modules)
    """

    def control(self, **kwargs):
        excess = self.production - self.power_demand

        if excess >= 0:
            # There is more PV production than house demand
            power_to_charge = self.charge(excess)
            self.power_to_grid = excess - power_to_charge
            self.power_to_house = self.power_demand
        else:
            # There is not enough PV production to meet house demand
            power_to_discharge = self.power_demand - self.production
            self.power_to_house = self.discharge(power_to_discharge) + self.production
            self.power_from_grid = self.power_demand - self.power_to_house
        return self.power_to_grid, self.power_from_grid, self.power_to_house

    def discharge(self, power: float) -> float:
        if self.soc < power:
            power = self.soc
            self.soc = 0
        else:
            self.soc -= power
        return power

    def charge(self, power: float) -> float:
        if self.soc + power > self.capacity:
            power = self.capacity - self.soc
            self.soc = self.capacity
        else:
            self.soc += power
        return power
