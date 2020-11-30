# UniFI-Dynamic-IP-UFW
Python script for updating a Ubuntu UniFi Controller UFW for dynamic WAN IP clients

# Requirements
Python 3 (v3.6 minimum)

The pyufw module.  Install with "pip3 install pyufw".

# How to use
Simply add the dynamic DNS hostnames to the hosts variable in the Python script.  Its a simple array so you just need ["host1.fq.dn","host2.fq.dn",etc,etc]

If you want to use the cron script, give it +x permissions and modify the path inside to point to where you put the Python script.  I find /etc/cron.hourly/ to be a sufficient place to put the cron script.

Obviously since the script interacts with UFW, it will need to be run sudoed or run as root.

Basic logging output will be written to /var/log/UFW-DynIP.log.  Alter this if you need more control over logging.
