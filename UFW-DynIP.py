import pyufw as ufw
import socket

hosts = [""]
ports = ["2222","8443","9090"]
addresses = []

status = ufw.status()
rules = status["rules"]

for host in hosts:
    ip = socket.gethostbyname(host)
    addresses.append(ip)

for address in addresses:
    for rule in rules:
        if address in rules[rule]:
            ufw.delete(rules[rule])

    for port in ports:
        new_rule = "allow from {} to any port {}".format(address, port)
        ufw.add(new_rule)
