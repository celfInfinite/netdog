# netdog
netdog is a python script that contains both a server and client scripts. The server script creates a reverse shell on the target machine and client
script creates a bind shell from the attacking machine.

## Installation
No isntallation is required, just download both client and server scripts. see usage on how to run the scripts.

## Usage
Create a reverse shell on the target machine: netdog.py -t 192.168.8.100 - p 8080
# This creates a reverse shell on the target machine by listening on port 8080
Create a bind shell on the attacking machine: netdog_client.py -192.168.8.100 -p 8080
# This creates a bind shell on attacking machines and gives access on port 8080

##Contribution
Pull requests are welcome. 
