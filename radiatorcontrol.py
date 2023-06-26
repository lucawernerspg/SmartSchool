from pyHS100 import SmartRadiatorValve

# IP address of your radiator valve
ip_address = "192.168.1.100"

# Connect to the radiator valve
radiator_valve = SmartRadiatorValve(ip_address)
radiator_valve.update()

# Print the current state of the radiator valve
print("Current temperature: {}°C".format(radiator_valve.temperature))
print("Target temperature: {}°C".format(radiator_valve.target_temperature))
print("Heating power: {}%".format(radiator_valve.heating_power))

# Set a new target temperature (in degrees Celsius)
new_target_temperature = 22
radiator_valve.target_temperature = new_target_temperature

# Print the updated target temperature
print("Updated target temperature: {}°C".format(radiator_valve.target_temperature))

# Turn on the radiator valve
radiator_valve.turn_on()

# Turn off the radiator valve
radiator_valve.turn_off()