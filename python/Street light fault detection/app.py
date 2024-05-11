from flask import Flask, render_template, request, jsonify
import mysql.connector
# import serial
# import time

app = Flask(__name__)

# MySQL database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root123@SA",
    database="ledsmart"
)
db_cursor = db_connection.cursor()

# Open serial connection
# ser = serial.Serial('COM18', 9600)  # Change 'COM3' to your serial port

# Function to execute the stored procedure and fetch data
def get_fault_data():
    query = "SELECT d.deviceid AS deviceid, d.location AS location, COALESCE(d2.light_status, 0) AS light_status, COALESCE(f.fault_status, 1) AS fault_status, d2.timestamp, CASE WHEN TIMESTAMPDIFF(MINUTE, d2.timestamp, NOW())<= 5 THEN 1 ELSE 0 END AS device_status  FROM loc_table d LEFT JOIN ( SELECT faultdev_id, fault_status, reporttime FROM fault_table WHERE (faultdev_id, reporttime) IN ( SELECT faultdev_id, MAX(reporttime) AS max_reporttime FROM fault_table GROUP BY faultdev_id )) f ON d.deviceid = f.faultdev_id LEFT JOIN ( SELECT deviceid, light_status, timestamp FROM sensor_data WHERE (deviceid, timestamp) IN ( SELECT deviceid, MAX(timestamp) AS max_timestamp FROM sensor_data GROUP BY deviceid)) d2 ON d.deviceid = d2.deviceid;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    return results

def get_active_faults():
    query = "SELECT COUNT(*) AS data FROM fault_table WHERE fault_status = 0;"
    db_cursor.execute(query)
    results = db_cursor.fetchone()
    return results[0]

def get_total_street_lights():
    query = "SELECT COUNT(DISTINCT deviceid)  from  loc_table"
    db_cursor.execute(query)
    results = db_cursor.fetchone()
    return results[0]

def get_resolved_faults():
    query = "SELECT COUNT(DISTINCT faultdev_id) AS count FROM fault_table WHERE fault_status = 1 AND reporttime >= DATE_SUB(NOW(), INTERVAL 4 WEEK);"
    db_cursor.execute(query)
    results = db_cursor.fetchone()
    return results[0]

def device_exists(device_id):
    db_cursor.execute("SELECT * FROM loc_table WHERE deviceid = %s", (device_id,))
    row = db_cursor.fetchone()
    return row is not None

def get_dev_map_data():
    query = "SELECT deviceid, location, lat, lon FROM loc_table"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    return results

def get_dev_drop_data():
    db_cursor.execute("SELECT deviceid FROM loc_table ORDER BY deviceid ASC")
    results = db_cursor.fetchall()
    
    return results

def get_dev_chart_data(device_id):
    db_cursor.execute("SELECT deviceid, light_status, timestamp FROM sensor_data WHERE deviceid = %s AND timestamp >= DATE_SUB(NOW(), INTERVAL 1 WEEK) ORDER BY timestamp ASC", (device_id,))
    results = db_cursor.fetchall()
    return results

def get_dev_chart_data_volt(device_id):
    db_cursor.execute("SELECT deviceid, voltage, timestamp FROM sensor_data WHERE deviceid = %s AND timestamp >= DATE_SUB(NOW(), INTERVAL 1 WEEK) ORDER BY timestamp ASC", (device_id,))
    results = db_cursor.fetchall()
    return results

def get_dev_chart_data_watt(device_id):
    db_cursor.execute("SELECT deviceid, watt, timestamp FROM sensor_data WHERE deviceid = %s AND timestamp >= DATE_SUB(NOW(), INTERVAL 1 WEEK) ORDER BY timestamp ASC", (device_id,))
    results = db_cursor.fetchall()
    return results

# Define routes

@app.route('/')
def index():
    # Call the function to fetch fresh data
    fault_data, total_street_lights, active_faults, resolved_faults = fetch_data()
    return render_template('index.html', fault_data=fault_data, total_street_lights=total_street_lights, active_faults=active_faults, resolved_faults=resolved_faults)

@app.route('/refresh-data')
def refresh_data():
    # Call the function to fetch fresh data
    fault_data, total_street_lights, active_faults, resolved_faults = fetch_data()
    return render_template('index.html', fault_data=fault_data, total_street_lights=total_street_lights, active_faults=active_faults, resolved_faults=resolved_faults)

def fetch_data():
    fault_data = get_fault_data()
    total_street_lights = get_total_street_lights()
    active_faults = get_active_faults()
    resolved_faults = get_resolved_faults()
    return fault_data, total_street_lights, active_faults, resolved_faults

# @app.route('/')
# def index():
#     fault_data = get_fault_data()
#     total_street_lights = get_total_street_lights()
#     active_faults = get_active_faults()
#     resolved_faults = get_resolved_faults()

#     return render_template('index.html', fault_data=fault_data, total_street_lights=total_street_lights, active_faults=active_faults, resolved_faults=resolved_faults)

@app.route('/submit_form', methods=['POST'])
def save_device_details():
    device_id = request.form['Device-ID']
    latitude = request.form['Latitude']
    longitude = request.form['Longitude']
    location = request.form['Location']

    if device_exists(device_id):
        return jsonify({'status': 'error', 'message': 'Device ID already exists'})
    else:
        db_cursor.execute("INSERT INTO loc_table (deviceid, lat, lon, location) VALUES (%s, %s, %s, %s)", (device_id, latitude, longitude, location))
        db_connection.commit()
        return jsonify({'status': 'success', 'message': 'Device details saved successfully'})

@app.route('/manual')
def manual():
    results = get_fault_data()
    return render_template('manual.html', devices=results)


@app.route('/map')
def map_view():
    map_data = get_dev_map_data()
    return render_template('map.html', map_data=map_data )

@app.route('/status')
def status():
    
    device_id = request.args.get('report-type')
    light_data = get_dev_chart_data(device_id)
    voltage_data = get_dev_chart_data_volt(device_id)
    watt_data = get_dev_chart_data_watt(device_id)

    return render_template('status.html', lightData=light_data, voltageData=voltage_data, wattData=watt_data)

@app.route('/config')
def config():
    query = "SELECT deviceid, location FROM loc_table ORDER BY deviceid ASC LIMIT 10"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    
    return render_template('config.html', devicedata=results)

@app.route('/report')
def report():
    dropdowndata = get_dev_drop_data()


    return render_template('report.html', dropdowndata=dropdowndata)

# # Serial data reading and database insertion loop
# try:
#     while True:
#         line = ser.readline().decode().strip()
#         data = line.split(',')

#         values = {}
#         for item in data:
#             key, value = item.split(': ')
#             values[key.strip()] = value.strip()

#         p_deviceid = values["Device_Name"]
#         p_voltage = values["LED_Voltage"]
#         p_current = values["LED_Current"]
#         p_watt = values["LED_Watts"]
#         p_tempcel = values["Temperature"]
#         p_tempfer = values["Temperature2"]
#         p_light_den = values["Light_Density"]
#         p_light_pin = values["Light_PIN"]
#         p_ir = values["IR"]
#         p_web_cond = values["Input"]

#         db_cursor.callproc("InsertSensorDataWithFault", (p_deviceid, p_voltage, p_current, p_watt, p_tempcel, p_tempfer, p_light_den, p_light_pin, p_ir, p_web_cond))
#         db_connection.commit()

#         print("Data inserted successfully.")

#         time.sleep(1)

# finally:
#     ser.close()
#     db_cursor.close()
#     db_connection.close()

if __name__ == '__main__':
    app.run(debug=True)
