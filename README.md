# ece480

### Pre-req:
- Clone the repository and ensure you have the correct packages in `main.py`
- The code to be deployed to the Arduino device is contained in `master_code/master_code.ino`

## Setting Up the System:
Two places for inserting the testing and flushing fluid are present in the physical system. 
Two ports exist for inserting the 9-volt batteries, once inserted, the system will automatically power on and be available for Bluetooth connection.
### Setting Up the Application: 
To prepare for testing,
1.	Once the Arduino is powered on, connect to it in your device's Bluetooth settings.
    - The device is named “HC-05.”
    - Its connection password is 1234

    **Note: If the Arduino has been power-cycled, you may need to “forget” the Bluetooth device and reconnect**
3.	Inspect the Python file and ensure the correct serial port is being used:
    - For Mac/Unix/Linux, the port name is likely /dev/tty.HC-05 You can check the port address by running ls /dev/tty.* from a terminal window
    - For Windows, the connection port is “COM5”
3.	Run the `main.py` Python file to start the application.
### Testing:
1.	First specify the number of sweeps and minimum and maximum sweeping voltages
    - Recommended settings for contamination testing:
      - Number of Sweeps: 3
      - Min Sweep Value: -2.5
      - Max Sweep Value: 2.5
2)	Once values are entered, clicking Start Experiment will begin the specified number of sweeps within the specified ranges.
    - If the experiment must be stopped before the sweeps have been completed, click the Stop Experiment button.
3)	The Reset button internally resets the number of sweeps, minimum voltage, and maximum voltage. The graph will start reset once the next experiment is configured and started.
4)	The Save Figure and Data button will export the data as a CSV file and the graph as a PNG file onto the user’s device in the directory where the Python file is located.
