import bluetooth
import sys

count = 0

nearby_devices = bluetooth.discover_devices() 
for bdaddr in nearby_devices:
    count += 1
    print count, ". " ,bluetooth.lookup_name( bdaddr )

selection = input("> ") - 1
print "You have selected", bluetooth.lookup_name(nearby_devices[selection])
bd_addr = nearby_devices[selection]
