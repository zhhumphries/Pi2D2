# Pi2D2
## Raspbery Pi Control System for R2D2
Pi2D2 is a simple control system for controlling an R2D2 and other droids via a connected bluetooth Gamepad.
## Current Features Include:
- Xbox Wireless Controller Support
- Sabertooth Dual 2x32 motor controller (Packetized Serial)

## Setup

- Connect Xbox Wireless Controller to Raspberry Pi (running Raspberry PI OS)
-- Run `bluetoothctl scan on`
-- Put Xbox Wireless Controller in Pairing mode (little button on top).
-- Take note of the MAC address that is associated with the Xbox Wireless Controller
-- Run `bluetoothctl pair [MAC_ADDRESS]` (MAC_ADDRESS is in the format of AA:AA:AA:AA:AA:AA)
-- Run `bluetoothctl connect [MAC_ADDRESS]`
-- Run `bluetoothctl scan off`
- Enable UART on the PI and disable serial0 console
-- Update /boot/cmdline.txt and remove the following text:
`console=serial0,115200`
-- Update /boot/config.txt and add the following to the end:
`enable_uart=1`
-- Restart the PI
- Connect Raspberry PI's Pin 6 Ground to 0V terminal on Sabertooth
- Connect Raspberry PI's Pin 8 UART0 TX to S1 terminal on Sabertooth
- Configure Sabertooth DIP switches for Serial Control
-- DIP Switch 1 and 2 set to off for Serial Control
-- DIP Switch 4 and 5 to on to use Packet Serial with a default address of 128
-- Wizard for setting DIP switches can be found here: https://www.dimensionengineering.com/datasheets/USBSabertoothDIPWizard/
- Install evdev and python-serial:
    ```sh
    sudo pip3 install evdev
    sudo pip3 install pyserial
    ```
- Installation of python code as a service is currently beyond the scope of this README
## Run
Currently, instructions assume you are going to SSH into the Raspberry PI and run the following manually. You can easily set this up as a service to happen automagically and restart automatically
- SSH into Raspberry PI from a computer connected to the same wireless network
- Navigate to the directory containing the Pi2D2 repo and run the following command
`python3 main.py`

## Known Issues
- In the event that the Xbox remote disconnects or turns off, the script will crash
- If the SSH session is terminated, the last command sent to the Sabertooth will continue
-- This only affects SSH approach for running the script.

## License

MIT
