import socketio
import time
import random

API_URL = "https://solar-glider-backend.onrender.com/" 

sio = socketio.Client()

def generate_sensor_data():
    return {
        "temperature": round(random.uniform(20, 35), 2),  
        "humidity": round(random.uniform(30, 80), 2)
    }

def send_data():
    sensor_data = generate_sensor_data()
    sio.emit('sensor_data', sensor_data) 
    print("Sent data:", sensor_data)


if __name__ == "__main__": 
    try:
        sio.connect(API_URL) 
        print("Connected to WebSocket server.")
        start_time = time.time()
        while time.time() - start_time < 10:
            send_data()
            time.sleep(0.5) 
        sio.disconnect()

    except KeyboardInterrupt:
        sio.disconnect()