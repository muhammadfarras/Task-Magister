import cv2
from util import get_limits, get_combined_mask
import threading
import time
import requests


def MainOpenCV():

    COLORS = {
        "Blue":  {"bgr": [255, 0,   0], "box_color": (255, 0,   0)},
        # "Red":  {"bgr": [0, 0,   255], "box_color": (0, 0, 255)}
    }

    cap = cv2.VideoCapture(1)

    # Waktu triger
    last_trigger = 0
    cooldown = 3

    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        center_x = (w // 2) + 100

        center_y = h // 2

        # For horizontal
        trigger_top = center_y - 40
        trigger_bottom = center_y + 40

        # Triger range
        trigger_left = center_x - 80
        trigger_right = center_x - 20

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for label, cfg in COLORS.items():
            mask = None
            for lower, upper in get_limits(cfg["bgr"], loose=True):
                part = cv2.inRange(hsv_frame, lower, upper)
                mask = part if mask is None else cv2.bitwise_or(mask, part)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                if cv2.contourArea(cnt) > 500:
                    x, y, bw, bh = cv2.boundingRect(cnt)

                    # Vertical
                    # box_center_x = x + bw // 2
                    box_center_y = y + bh // 2 # Horizontal
                    
                    current_time = time.time()
                    # Check which side of the line the object is on
                    if box_center_y < center_x:
                        # Wait the servo
                        side = "LEFT"
                    else:
                        # Run the servo to move the object
                        side = "RIGHT"

                    # if trigger_left <= box_center_x <= trigger_right:
                    if trigger_top <= box_center_y <= trigger_bottom:
                        side = "TRIGGER"

                        if current_time - last_trigger > cooldown:
                            trigger_open_gate_async(request_open_the_gate)
                            last_trigger = current_time

                    cv2.rectangle(frame, (x, y), (x + bw, y + bh), cfg["box_color"], 2)
                    cv2.putText(frame, f"{label} {side}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, cfg["box_color"], 2)

        # Draw vertical center line
        cv2.line(frame, (0, trigger_top), (w, trigger_top), (0, 255, 0), 2)
        cv2.line(frame, (0, trigger_bottom), (w, trigger_bottom), (0, 255, 0), 2)
        # cv2.line(frame, (trigger_left, 0), (trigger_left, h), (0, 255, 0), 2)
        # cv2.line(frame, (trigger_right, 0), (trigger_right, h), (0, 255, 0), 2)
        cv2.putText(frame, "CENTER", (center_x + 5, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        cv2.imshow('Color Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def request_open_the_gate():
    url = "http://192.168.0.152/open_gate"
    resp = requests.post(url, json={"text": "open the gate"})
    print(resp.text)

def request_close_the_gate():
    url = "http://192.168.0.152/close_gate"
    resp = requests.post(url, json={"text": "close the gate"})
    print(resp.text)

def trigger_open_gate_async(function):
    thread = threading.Thread(target=function)
    thread.daemon = True  # background thread, won't block exit
    thread.start()

if __name__ == '__main__':
    MainOpenCV()