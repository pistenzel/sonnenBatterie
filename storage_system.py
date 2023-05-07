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
        self.max_power = 0
        self.voltage = 0
        self.current = 0
        self.power = 0
        self.grid_frequency = 0
        self.grid_voltage = 0


class BatteryModule:
    """
    Battery module (BMS): each of the battery packs that can be connected into a sonnenBatterie storage system.
    Values available to be read from each of them are:
    - Module temperature in Celsius degrees
    - Module voltage in Volts.
    - Maximum power that the battery module can charge or discharge in Watts.
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.soc = 0
        self.temperature = 0
        self.voltage = 0
        self.max_power = 0


class StorageSystem:
    """
    sonnenBatterie storage system. It can release energy from the battery modules into the house grid or store energy
    from the house grid into the battery modules. Available configurations and values are:
    - Power command in Watts. Commands can be:
        - charge: positive Watts value
        - discharge: negative Watts value
    - Any value available from any of the internal components (inverter and battery modules)
    """

    def __init__(self, controller, inverter, batteries):
        self.controller = controller
        self.inverter = inverter
        self.batteries = batteries
        self.capacity = sum(b.capacity for b in self.batteries)
        self.soc = sum(b.soc for b in self.batteries)

    def control(self, pv_panel, house):
        production = pv_panel['power']
        power_demand = house['power']
        power_to_grid = power_from_grid = 0
        excess = production - power_demand

        if excess >= 0:
            # There is more PV production than house consumption
            power_to_charge = self.charge(excess)
            power_to_grid = excess - power_to_charge
            power_to_house = self.discharge(power_demand)
        else:
            # There is not enough PV production to meet house consumption
            power_to_house = self.discharge(power_demand)
            if self.soc < self.capacity:
                power_from_grid = self.charge(self.capacity - self.soc - power_to_house)
            else:
                power_from_grid = 0

        # Todo Use result schema or class
        return {
            'power_to_grid': power_to_grid,
            'power_to_house': power_to_house,
            'power_from_grid': power_from_grid
        }

    def discharge(self, power):
        if self.soc < power:
            power = self.soc
            self.soc = 0
        else:
            self.soc -= power
        return power

    def charge(self, power):
        if self.soc + power > self.capacity:
            power = self.capacity - self.soc
            self.soc = self.capacity
        else:
            self.soc += power
        return power
