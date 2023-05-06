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

    def control(self, production, consumption):
        pass

    def charge(self, power):
        pass

    def discharge(self, power):
        pass

    @property
    def capacity(self):
        return sum(b.capacity for b in self.batteries)

    @property
    def soc(self):
        return sum(b.soc for b in self.batteries)
