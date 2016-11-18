#!/usr/bin/env python
from __future__ import print_function
import jinja2
import csv
import pprint
import sys
import os.path

#load in values from pnp_config.py file, values represent template directory, files, and devices.
from pnp_config import CONFIGS_DIR, TEMPLATE, DEVICES, KEYVALUE

#output a list of dictionaries from device CSV file. Each dictionary represents a row from the CSV, AKA a device and its config values.
def csv_dict_list(devices, role):
    reader = csv.DictReader(open(devices, 'rb'))
    dict_list = []
    for line in reader:
        if role in line.itervalues():
            dict_list.append(line)
    return dict_list

#Generate Configuration from CSV, Template, and unique role or ID.
def build_templates(template_file, devices, role):
    #Create a List of Dictionaries from the CSV file that contain the keyword or role.
    dictList = csv_dict_list(devices, role)
    #setup template environment paths and directories
    templateLoader = jinja2.FileSystemLoader( searchpath="." )
    env = jinja2.Environment( loader=templateLoader )
    #Add logic here if we want to use different templates based on models, spoke or hub roles, etc.
    template = env.get_template(template_file)

    #Generate Configuration for each Dictionary in the List.
    for dictionary in dictList:
        config = template.render(dictionary)
        config_filename = dictionary['hostName'] + '-config'
        with open(config_filename, 'w') as config_file:
            config_file.write(config)
            print("wrote file: %s" % config_filename)

#think about changing spoke argument to pull from pnp_config.py
if __name__ == "__main__":
    build_templates(TEMPLATE, DEVICES, 'Spoke')