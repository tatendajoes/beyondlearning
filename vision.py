import cv2 as cv
from ultralytics import YOLO
from metrics import Metrics
import pandas as pd
import time as time
class VideoCapture:
    def __init__(self, src=0):
        self.cap = cv.VideoCapture(src)
        self.fps = self.cap.get(cv.CAP_PROP_FPS)
        self.fps = self.cap.get(cv.CAP_PROP_FPS)
        self.model = YOLO(r"models\best3.pt")
        self.labels = {0: 'focused',
                       1: 'unfocused'}
        self.buffer = {'label': [],
                       'frame': [],
                       'timestamp': [],
                       'confidence': []}
        self.frame_count = 0
        if not self.cap.isOpened():
            raise ValueError("Could not open video source")

    def read(self):
        ret, frame = self.cap.read()
        return ret, frame if ret else None

    def release(self):
        self.cap.release()
        cv.destroyAllWindows()

    def process_frame(self, frame):
        results= self.model(frame, stream=True, conf=0.55)  # predict on the frame
        for r in results:
            boxes = r.boxes  # Boxes object for bbox outputs
            if boxes is not None:
                for box in boxes.data:
                    x1, y1, x2, y2 = map(int, box[:4])
                    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw rectangle on frame
                    # Optional: Draw label and confidence
                    label = f"{self.labels[int(box[5])]} {box[4]:.2f}"
                    cv.putText(frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    self.buffer['label'].append(self.labels[int(box[5])])
                    self.buffer['frame'].append(self.frame_count)
                    self.buffer['timestamp'].append(self.frame_count / self.fps)  # Calculate timestamp
                    self.buffer['confidence'].append(box[4]) 
        return frame
    def show(self, frame):
        cv.imshow("Video", frame) 
        self.frame_count += 1  # Increment frame count
        return self.frame_count if self.frame_count else None
    def wait(self, delay=1):
        return cv.waitKey(delay) & 0xFF == ord('q')
    
#------------------------------------------------------------------------
# Main function to run the video capture and processing
if __name__ == "__main__":
    metrics = Metrics()
    #Get user input for classid, classdate, classtime, classattendance
    show= False
    classid = input("Enter class ID: ")
    classdate = input("Enter class date (YYYY-MM-DD): ")
    classtime = input("Enter class time (HH:MM): ")
    classattendance = input("Enter class attendance: ")
    # Create a header dictionary with user input
    header = {'classid': classid,
              'classdate': classdate,
              'classtime': classtime,
              'classattendance': classattendance}
    video_capture = VideoCapture(src=r'testvideos\vv2.mp4')  # Use 0 for webcam or provide a video file path
    while True:
        timer = time.time()
        ret, frame = video_capture.read()
        if not ret:
            break
        processed_frame = video_capture.process_frame(frame)
        if show:
            frame_count = video_capture.show(processed_frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    # Metrics calculation and display
    metrics.get_buffer(video_capture.buffer)
    metrics.dump_metrics(header=header)
    metrics.display_metrics()
    metrics.plot_metrics()
    