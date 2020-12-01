#!/usr/bin/env python3

import socket, logging, sys
import pyufw as ufw

logging.basicConfig(
        filename="/var/log/UFW-DynIP.log",
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(message)s"
        )

# You only need to modify the hosts variable to fit your needs.
# You could add more ports if you want, but what is here is all that you need.
# Adding port 9090 is optional if you followed the online guides and installed cockpit
hosts = [""]
ports = ["2222", "8443"]

# Needed empty array
addresses = []

# Get the list of rules
status = ufw.status()
rules = status["rules"]

# Get the dynamic addresses from the hosts list
for host in hosts:
    try:
        ip = socket.gethostbyname(host)
        addresses.append(ip)
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
        try:
            new_rule = "allow from {} to any port {}".format(address, port)
            ufw.add(new_rule)
            logging.info("Added rule {}".format(new_rule))
        except:
            logging.error("Error creating rule {}".format(rules[rule]))
