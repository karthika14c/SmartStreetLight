import serial
import mysql.connector
import time

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root123@SA",
    database="ledsmart"
)
db_cursor = db_connection.cursor()

# Open serial connection
ser = serial.Serial('COM18', 9600)  # Change 'COM3' to your serial port

try:
    while True:
        # Read a line from the serial port
        line = ser.readline().decode().strip()

        # Split the line into data fields
        data = line.split(',')


        # Parse each data field
        values = {}
        for item in data:
            key, value = item.split(': ')
            values[key.strip()] = value.strip()

        # Insert data into the database
        #db_cursor.callproc("InsertSensorDataWithFault", ("Light1", 0.14, 0.14, 0, 28, 86, 986, 0, 1, 2))
        #db_connection.commit()


        p_deviceid = values["Device_Name"]
        p_voltage = values["LED_Voltage"]
        p_current = values["LED_Current"]
        p_watt = values["LED_Watts"]
        p_tempcel = values["Temperature"]
        p_tempfer = values["Temperature2"]
        p_light_den = values["Light_Density"]
        p_light_pin = values["Light_PIN"]
        p_ir = values["IR"]
        p_web_cond = values["Input"]
        # Call the stored procedure
        db_cursor.callproc("InsertSensorDataWithFault", (p_deviceid, p_voltage, p_current, p_watt, p_tempcel, p_tempfer, p_light_den, p_light_pin, p_ir, p_web_cond))

        # Commit the transaction
        db_connection.commit()

        print("Data inserted successfully.")
        
        # Wait for 1 second before reading the next data
        time.sleep(1)

finally:
    # Close connections
    ser.close()
    db_cursor.close()
    db_connection.close()
