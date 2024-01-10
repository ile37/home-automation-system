#!/usr/bin/env python3

import sys
import os

def main(device_node):

    if device_node == "1-1.2":	
        message = f"USB device connected: {device_node}"
        os.system(f'wall "{message}"')

#    with open('/home/ilari/home_automation/usb_connection/usb_log.txt', 'a') as log_file:
#       log_file.write(f"USB device connected: {device_node}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: usb_script.py <device_node>")
        sys.exit(1)

    device_node = sys.argv[1]
    main(device_node)

