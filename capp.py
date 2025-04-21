from vision import VideoCapture
from metrics import Metrics

class App:
    def __init__(self, src, show=False):
        self.video_capture = VideoCapture(src)
        self.metrics  = Metrics()
        self.show= show
    
    def run(self):
#Get user input for classid, classdate, classtime, classattendance
        classid = input("Enter class ID: ")
        classdate = input("Enter class date (YYYY-MM-DD): ")
        classtime = input("Enter class time (HH:MM): ")
        classattendance = input("Enter class attendance: ")
        # Create a header dictionary with user input
        header = {'classid': classid,
                    'classdate': classdate,
                    'classtime': classtime,
                    'classattendance': classattendance}  # Use 0 for webcam or provide a video file path
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break
            processed_frame = self.video_capture.process_frame(frame)
            if self.show:
                frame_count = self.video_capture.show(processed_frame)
            self.video_capture.wait()
        self.video_capture.release()
        # Metrics calculation and display
        self.metrics.get_buffer(self.video_capture.buffer)
        self.metrics.dump_metrics(header=header)
        self.metrics.display_metrics()
        self.metrics.plot_metrics()
        
if __name__ == "__main__":
    app = App(src=r'testvideos\vv2.mp4', show=True) 
    app.run()