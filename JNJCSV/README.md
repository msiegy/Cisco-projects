Python script that uses Jinja2 Templates to output configuration files based on input from a CSV File.
Inspired by Adam Radford @ https://github.com/CiscoDevNet/apic-em-samples-aradford

The CSV File (configvars.csv) containing the device configuration values is converted to a List of Dictionaries. The List of Dictionaries is then referenced and applied to a Jinja2 template in order to build out a complete configuration. Because dictionaries and the render template function is used the values within the CSV file do not need to be in any particular order.

FILES
pnp_config.py - Text file for setting environment values. working directory and template file name. may move role/id argument to this file
buildconfigurations.py - Main python script that generates configuration files.
configvars.csv - CSV file containing Device names and configuration values.
config_templateIWAN.jnj - Jinja2 sample template containing small portion of DMVPN configuration
