#!/usr/bin/env python3

import socket, logging, sys, configparser, os
import pyufw as ufw
from logging.handlers import RotatingFileHandler

# Move to the script's directory
os.chdir(sys.path[0])

# Read in the config file
config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(
        handlers=[RotatingFileHandler(config.get('main_config', 'logfile'), maxBytes=10000, backupCount=10)],
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s"
        )

# You only need to modify the hosts variable to fit your needs.
# You could add more ports if you want, but what is here is all that you need.
# Adding port 9090 is optional if you followed the online guides and installed cockpit
hosts = config.get('main_config', 'hosts').split(',')
ports = config.get('main_config', 'ports').split(',')
prev_addresses = config.get('main_config', 'prev_addresses')

# Needed empty array
new_addresses = []

# Get the list of rules
status = ufw.status()
rules = status["rules"]

# Get the dynamic addresses from the hosts list
for host in hosts:
    try:
        new_addresses.append(socket.gethostbyname(host))
    except:
        logging.error("Error looking up host {}".format(host))
        sys.exit()

# Check for & delete the old rules first
if prev_addresses != '':
    old_addresses = prev_addresses.split(',')
    for address in old_addresses:
        for rule in rules:
            if address in rules[rule]:
                try:
                    ufw.delete(rules[rule])
                    logging.info("Deleted rule {}".format(rules[rule]))
                except:
                    logging.error("Error deleting rule {}".format(rules[rule]))

# Refresh the list of rules
status = ufw.status()
rules = status["rules"]

# Add in the new rules
for address in new_addresses:
    # Double check for existing rules
    for rule in rules:
        if address in rules[rule]:
            try:
                ufw.delete(rules[rule])
                logging.info("Deleted rule {}".format(rules[rule]))
            except:
                logging.error("Error deleting rule {}".format(rules[rule]))

    # Create the new rules
    for port in ports:
        new_rule = "allow from {} to any port {}".format(address, port)
        try:
            ufw.add(new_rule)
            logging.info("Added rule {}".format(new_rule))
        except:
            logging.error("Error creating rule {}".format(new_rule))

config['main_config']['prev_addresses'] = ",".join(new_addresses)

with open('config.ini', 'w') as configfile:
    config.write(configfile)