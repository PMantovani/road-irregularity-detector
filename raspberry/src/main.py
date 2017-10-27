import time
import gps
import accelerometer
import threading
import requests
import json

if __name__ == "__main__":
    api_url = 'http://localhost:8080/api.php'
    accel_scale = 8
    accel_limit = 4
    speed_limit = 30
    sleep_after_request = 10
    sleep_repeat = 0.01

    run_event = threading.Event()
    run_event.set()

    # starts gps thread
    my_gps = gps.GPS(run_event)
    my_gps.start()

    # starts accelerometer thread
    my_accelerometer = accelerometer.Accelerometer(run_event)
    my_accelerometer.start()
    my_accelerometer.set_accelerometer_scale(accel_scale)

    # keeps forever in the loop until a keyboard interrupt is detected
    try:
        while True:
            # gps signal not available or speed under 30km/h
            if not my_gps.signal_validity or my_gps.speed < speed_limit:
                continue
            # irregularity detected! send request to server
            if abs(my_accelerometer.accel_z) > accel_limit:
                req_json = json.dumps({'latitude': my_gps.latitude, 'longitude': my_gps.longitude,
                                       'accelerometer': my_accelerometer.accel_z, 'speed': my_gps.speed})
                req_return = requests.post(api_url, data=req_json)
                time.sleep(sleep_after_request)

            time.sleep(sleep_repeat)

    except KeyboardInterrupt:
        run_event.clear()
        my_gps.join()
        my_accelerometer.join()
        print "Closed all threads successfully!"
