#!/bin/bash
rsync -a --delete -e ssh ~/Projects/RaspberryPions pi@192.168.2.22:~/ &> /dev/null

# Do the same for all peon ips
