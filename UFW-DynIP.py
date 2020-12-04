#!/usr/bin/env python3

import socket, logging, sys, configparser
import pyufw as ufw

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(
        filename=config.get('main_config', 'logfile'),
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s"
        )

# You only need to modify the hosts variable to fit your needs.
# You could add more ports if you want, but what is here is all that you need.
# Adding port 9090 is optional if you followed the online guides and installed cockpit
hosts = config.get('main_config', 'hosts').split()
ports = config.get('main_config', 'ports').split()

# Needed empty array
addresses = []

# Get the list of rules
status = ufw.status()
rules = status["rules"]

# Get the dynamic addresses from the hosts list
for host in hosts:
    try:
        addresses.append(socket.gethostbyname(host))
    except:
        logging.error("Error looking up host {}".format(host))
        sys.exit()

# Main loop
for address in addresses:
    # Delete the old rules first
    for rule in rules:
        if address in rules[rule]:
            try:
                ufw.delete(rules[rule])
                logging.info("Deleted rule {}".format(rules[rule]))
            except:
                logging.error("Error deleting rule {}".format(rules[rule]))

    # And add in the new rules
    for port in ports:
        new_rule = "allow from {} to any port {}".format(address, port)
        try:
            ufw.add(new_rule)
            logging.info("Added rule {}".format(new_rule))
        except:
            logging.error("Error creating rule {}".format(new_rule))
