import socketio
import time
import random

API_URL = "https://solar-glider-backend.onrender.com/"

sio = socketio.Client()

def generate_sensor_data(elapsed_time, prev_data):
    # Battery decreases linearly
    battery_percentage = max(100 - (elapsed_time / 30) * 100, 0)
    
    # Solar panels cleaned increases every 5 seconds
    cleaned_panels = elapsed_time // 5  

    # Move grid location by one adjacent step
    x, y = prev_data["grid_location"]
    new_x = max(0, min(19, x + random.choice([-1, 0, 1])))  # Move -1, 0, or 1
    new_y = max(0, min(19, y + random.choice([-1, 0, 1])))
    grid_location = (new_x, new_y)

    # Smooth gyroscope data
    def smooth_change(value, change_range=(-2, 2)):  # Small smooth change
        return round(value + random.uniform(*change_range), 2)

    gyro_data = {
        "pitch": smooth_change(prev_data["gyro"]["pitch"]),
        "roll": smooth_change(prev_data["gyro"]["roll"]),
        "yaw": smooth_change(prev_data["gyro"]["yaw"]),
    }

    return {
        "battery_percentage": round(battery_percentage, 2),
        "cleaned_panels": cleaned_panels,
        "grid_location": grid_location,
        "gyro": gyro_data
    }

# Initialize sensor data
sensor_data = {
    "battery_percentage": 100,
    "cleaned_panels": 0,
    "grid_location": (random.randint(0, 19), random.randint(0, 19)),
    "gyro": {"pitch": 0, "roll": 0, "yaw": 0}
}

def send_data(elapsed_time):
    global sensor_data
    sensor_data = generate_sensor_data(elapsed_time, sensor_data)  # Update global sensor data
    sio.emit('sensor_data', sensor_data)
    print("Sent data:", sensor_data)

if __name__ == "__main__":
    try:
        sio.connect(API_URL, namespaces=['/'])  # Ensure proper connection
        if not sio.connected:
            print("Failed to connect to WebSocket server.")
        else:
            print("Connected to WebSocket server.")

            start_time = time.time()
            while time.time() - start_time < 10:
                elapsed = time.time() - start_time  # Calculate elapsed time
                send_data(elapsed)  # ✅ Pass elapsed time correctly
                time.sleep(1)  # Send data every second

        sio.disconnect()
        print("Disconnected from server.")

    except KeyboardInterrupt:
        sio.disconnect()
        print("Connection closed manually.")
