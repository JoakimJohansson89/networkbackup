

import time
import os
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# Device configuraiton for Fortinet
devices = [
    {
        "device_type": "fortinet",
        "host": "192.168.1.1", # Fortinet Device IP
        "username" : "your_username",
        "password" : "your_password",
        "command": "show full-configuration"
    },
    {
        "device_type": "dlink_ds",
        "host": "192.168.2.1", # D-Link device IP
        "username": "dlink_user",
        "password": "dlink_password",
        "command": "show running-config",
    },
]

def is_reachable(host):
    """Checks if a device is reachable via ping"""
    response = os.system(f"ping -c 1 {host} > /dev/null 2>&1")
    return response == 0


def save_configuration(device):
    """Extracts and saves configuration from a device"""
    connection = None # Initialize connection variable
    # Connect to the device
    try:
        print(f"Connecting to {device['host']} ({device['device_type']})...")
        connection = ConnectHandler(**device)

        # Enter enable mode if required (optional for Fortinet, not Cisco though)
        # connection.enable() # Fortinet does not usually require enable

        # Get the running configuration
        print(f"Retriving configuraiton using command: {device['command']}...")
        config = connection.send_command(device["command"])

        # Save the configuration to a file
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{device['device_type']}_config_{device["host"]}_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(config)

        print(f"Configuration saved to {filename}")
    
    except NetmikoTimeoutException:
        print(f"Connection to {device['host']} timed out")
    except NetmikoAuthenticationException:
        print(f"Authenticatrion failed for {device['host']}")
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        # Disconnect only if connection is established
        if connection:
            connection.disconnect()

if __name__=="__main__":
    while True:
        for device in devices:
            save_configuration(device)
        # Wait for a specified time before the next extraction (seconds)
        time.sleep(60)