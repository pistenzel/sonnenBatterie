# sonnenBatterie

## Scenario Description
As you already know Sonnen is market leader of battery storage systems in Europe. Our product is called
sonnenBatterie (SB).
A SB has three components: an inverter, the battery modules and a controller. The different
components of the system can be provided by different vendors. The inverter, batteries and controller
are installed together in a storage system.

Typically, the SB is installed in a household, so the house owner can save money by not using the energy
that comes from the grid.
One of the major features of the SB is to charge or discharge based on photovoltaics and consumption.
The system can get energy from a photovoltaic (PV) panel besides getting it from the grid, or it can use
the Storage system itself.
The basic energy algorithm is as follows:
1. If there is more PV production than house consumption, the following priority order should be
followed:
   1. Then the storage system can be charged with the surplus.
   2. The remaining power can go to the grid.
2. In the opposite case:
   1. Storage should supply the power to the house.
   2. If power is still missing, the grid should provide it.

All this logic is usually handled by the controller.

## System description
Photovoltaic panel: produces energy from the sun radiation. Values that can be read:
* Amount of power the PV is producing in Watts
* Voltage that the PV is producing in Volts
* Current that the PV is producing in Amps

Grid: main connection from the house to the utility provider grid. Values that can be read:
* Amount of power that is sold and bought to/from the utility provider.
* Grid voltage in Volts
* Grid frequency in Hertz

* House: measurement point of all house connected loads. Values that can be read:
* Amount of power that is going into the house in Watts
* Voltage of the house grid
* Frequency of the house grid
* Current flowing into the house in Amps

Inverter: device inside the sonnenBattery in charge of controlling the power flow to the
batteries. Available values to read are:
* Maximum power that the inverter can charge/discharge in Watts
* Battery voltage in Volts
* Battery current that is flowing to/from inverter in Amps
* Power inverter is releasing/storing in the batteries in Watts
  * positive value notates inverter power is flowing into the batteries (charging)
  * negative value notates battery power is flowing into the inverter (discharging)
* Inverter sensed grid frequency in Hertz
* Inverter sensed grid Voltage in Volts

Battery module (BMS): each of the battery packs that can be connected into a sonnenBatterie
storage system. Values available to be read from each of them are:
* Module temperature in Celsius degrees
* Module voltage in Volts.
* Maximum power that the battery module can charge or discharge in Watts.

Storage: sonnenBatterie storage system. It can release energy from the battery modules into
the house grid or store energy from the house grid into the battery modules. Available
configurations and values are:
* Power command in Watts. Commands can be:
  * charge: positive Watts value
  * discharge: negative Watts value
* Any value available from any of the internal components (inverter and battery modules)

EM controller: handles the energy logic and issues all necessary commands to each of the
devices.

All these parameters could be used to compute the power management following the priorities
described in the scenario description.