import json
import random
import datetime
import requests
import time

# Define the IP address to send the JSON data
ip_address = "192.168.1.8"

while True:
    # Load the JSON data
    with open("data.json", "r") as file:
        data = json.load(file)

    # Update the data for the first patient
    patient_data = data["patients_data"][0]
    patient_data["name"] = "John Doe"
    patient_data["age"] = 35
    patient_data["userID"] = "JD001"

    # Maintain 5 rows of data
    if len(patient_data["data"]) >= 5:
        patient_data["data"].pop(0)  # Remove the oldest row

    # Generate the current timestamp
    current_timestamp = datetime.datetime.now().isoformat()

    # Generate random values for SPO2 and pulse
    spo2 = random.randint(0, 100)
    pulse = random.randint(0, 100)

    # Append the new row of data
    patient_data["data"].append({
        "timestamp": current_timestamp,
        "spo2": spo2,
        "pulse": pulse
    })

    # Convert the updated data to JSON
    updated_data = json.dumps(data)

    # Write the updated data back to the file
    with open("data.json", "w") as file:
        file.write(updated_data)

    # Send the JSON data to the specified IP address over WiFi
    url = f"http://{ip_address}/update_data"
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=updated_data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Data sent successfully.")
    else:
        print("Failed to send data.")

    # Wait for 1 minute before sending the next data
    time.sleep(60)
