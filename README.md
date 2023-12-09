# ece480

## Setting Up the System:
Two places for inserting the testing and flushing fluid are present on the physical system. 
Two ports exist for inserting the 9-volt batteries, once inserted, the system will automatically power on and be available for Bluetooth connection.
### Setting Up the Application: 
To prepare for testing,
1.	Once the Arduino is powered on, connect to it in your devices Bluetooth settings. Note: If the device has been power-cycled, you may need to “forget” the device and reconnect
a.	The device is named “HC-05.”
b.	Its connection password is 1234
2.	Inspect the Python file and ensure the correct serial port is being used:
a.	For Mac/Unix/Linux, the port name is likely /dev/tty.HC-05 You can check the port address by running ls /dev/tty.* from a terminal window
b.	For Windows, the connection port is “COM3”
3.	Run the python file to start the application.
### Testing:
1)	First specify the number of sweeps and minimum and maximum sweeping voltages
a)	Recommended settings for contamination testing:
i)	Number of Sweeps: 3
ii)	Min Sweep Value: -2.5
iii)	Max Sweep Value: 2.5
2)	Once values are entered, clicking Start Experiment will begin the specified number of sweeps within the specified ranges.
a)	If the experiment must be stopped before the sweeps have completed, click the Stop Experiment button.
3)	The Reset button internally resets the number of sweeps, minimum voltage, and maximum voltage. The graph will start reset once the next experiment is configured and started.
4)	The Save Figure and Data button will export the data as a CSV file and the graph as a PNG file onto the user’s device in the directory where the Python file is located.
![image](https://github.com/jmessing-29/ece480/assets/102541893/6109c9e4-286d-44a1-b51f-cf5020f5a85a)
