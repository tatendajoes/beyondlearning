import cv2 as cv
from ultralytics import YOLO
import pandas as pd

cap = cv.VideoCapture('vv3.mp4') 

# Open the video file
fps = cap.get(cv.CAP_PROP_FPS)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

model= YOLO("best.pt")  
labels= {0:'focused',
         1: 'sleep',
         2: 'study',
         3:'onphone',
         4:'sleeping',
         5:'writing'} 

buffer= {'label': [],
         'frame': [],
         'timestamp': [],
            'confidence': []
         }  # Initialize buffer to store labels and timestamps
frame_count = 0  # Initialize frame count
while True:
    ret, frame = cap.read()
    if not ret:
        break
    results= model(frame, stream=True, conf=0.45)  # predict on the frame
    for r in results:
        boxes = r.boxes  # Boxes object for bbox outputs
        if boxes is not None:
            for box in boxes.data:
                x1, y1, x2, y2 = map(int, box[:4])
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw rectangle on frame
                # Optional: Draw label and confidence
                label = f"{labels[int(box[5])]} {box[4]:.2f}"
                cv.putText(frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                buffer['label'].append(labels[int(box[5])])
                buffer['frame'].append(frame_count)
                buffer['timestamp'].append(frame_count / fps)  # Calculate timestamp
                buffer['confidence'].append(box[4]) 
    cv.imshow("Video", frame)  # Display the frame with predictions 
    frame_count += 1  # Increment frame count
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()  # Release the video capture object
cv.destroyAllWindows()  # Close all OpenCV windows

df = pd.DataFrame(buffer)  # Create DataFrame from buffer
print(df.head())
df.to_csv('output.csv', index=False)  # Save DataFrame to CSV file
print("CSV file saved successfully.")