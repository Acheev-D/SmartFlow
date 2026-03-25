"""
SmartFlow AI: Edge Vision Sensor (Proof of Concept)
---------------------------------------------------
This script simulates the software running on the Edge Device (e.g., NVIDIA Jetson)
attached to the traffic light camera. 

It uses YOLOv8 to detect vehicles in a video stream, counts them in a specific 
Region of Interest (ROI), and calculates the "Lane Pressure" to send to the controller.

Prerequisites:
pip install opencv-python ultralytics numpy
"""

import cv2
import numpy as np
from ultralytics import YOLO
import time

def main():
    print("--- SmartFlow Edge Sensor Initializing ---")
    
    # 1. Load the pre-trained YOLOv8 model (Nano version for fast Edge computing)
    print("Loading YOLOv8n model...")
    model = YOLO('yolov8n.pt') 
    
    # 2. Open a video stream
    # Changed to 0 to automatically use your laptop's primary webcam!
    video_source = 0 
    
    # Adding cv2.CAP_DSHOW forces Windows to use DirectShow, fixing the "black screen" issue
    cap = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
    
    # Fallback just in case DirectShow fails (though highly unlikely)
    if not cap.isOpened():
        print("DirectShow failed, trying default backend...")
        cap = cv2.VideoCapture(video_source)
        
    if not cap.isOpened():
        print(f"Error: Could not open webcam (source {video_source}).")
        print("Tip: Check if another app (like Zoom or Teams) is using your camera.")
        return

    # Define the Region of Interest (ROI) - e.g., the 'waiting zone' near the stop line
    # Format: [x1, y1, x2, y2] - adjust based on your camera angle
    roi = [100, 200, 500, 400] 
    
    # Vehicle classes in COCO dataset (2: car, 3: motorcycle, 5: bus, 7: truck, 0: person)
    # Added '0' (person) temporarily so you can test it on yourself with the webcam!
    vehicle_classes = [0, 2, 3, 5, 7]

    print("Sensor Online. Monitoring Lane Pressure...")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success or frame is None:
            # If the frame is still completely empty, skip and wait for the camera to warm up
            continue
            
        # Resize for faster processing on "Edge" hardware
        frame = cv2.resize(frame, (640, 480))
        
        # 3. Run Object Detection
        results = model(frame, stream=True, verbose=False)
        
        vehicle_count = 0
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Class ID
                cls = int(box.cls[0])
                
                # Filter for vehicles (and people for webcam testing)
                if cls in vehicle_classes:
                    # Bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Calculate center point of the object
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    
                    # Check if the object is inside our ROI (the stop line queue)
                    if roi[0] < cx < roi[2] and roi[1] < cy < roi[3]:
                        vehicle_count += 1
                        
                        # Draw bounding box (Green = counted)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                    else:
                        # Draw bounding box (Gray = ignored/moving traffic)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (150, 150, 150), 1)

        # 4. Calculate "Lane Pressure" (The core SmartFlow algorithm)
        # In reality, this data is sent via JSON/MQTT to the signal controller
        lane_pressure = vehicle_count * 1.5 
        
        # --- Visualization for Demo Purposes ---
        
        # Draw ROI Box
        cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), (255, 0, 0), 2)
        cv2.putText(frame, "Detection Zone", (roi[0], roi[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Draw HUD
        cv2.rectangle(frame, (10, 10), (250, 100), (0, 0, 0), -1)
        cv2.putText(frame, f"SmartFlow Sensor", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Objects in Zone: {vehicle_count}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Lane Pressure: {lane_pressure}", (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        cv2.imshow("SmartFlow Edge AI - Live View", frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        time.sleep(0.03) # Limit framerate to simulate Edge device constraints

    cap.release()
    cv2.destroyAllWindows()
    print("Sensor Offline.")

if __name__ == "__main__":
    main()