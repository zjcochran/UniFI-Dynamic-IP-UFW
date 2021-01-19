# UniFi-Dynamic-IP-UFW
Python script for updating a Ubuntu UniFi Controller UFW for dynamic WAN IP clients and locking down access to the cloud server to just the WAN IP addresses of the clients.

# Requirements
Python 3

The pyufw module.  Install with "pip3 install pyufw".

UniFi Controller was installed per Crosstalk Solution's excellent guide:

https://crosstalksolutions.com/definitive-guide-to-hosted-unifi/

# How to use
Simply edit config.ini to suit your needs (place config.ini in the same directory as the python script):

```
logfile = /var/log/UFW-DynIP.log
hosts = host1.fq.dn,host2.fq.dn
ports = 2222,8443
prev_addresses = 
```

For the hosts and ports, put a comma in between each item like in the example and the script will pick it all up automatically.  You will not need to modify prev_addresses since that will be filled in automatically.

If you want to use the cron script, give it +x permissions and modify the path inside to point to where you put the Python script.  I find /etc/cron.hourly/ to be a sufficient place to put the cron script.  You can also give +x directly to the Python script and run it directly.

Obviously since the script interacts with UFW, it will need to be run sudoed or run as root.

Basic logging output will be written to /var/log/UFW-DynIP.log.  Alter this if you need more control over logging.
