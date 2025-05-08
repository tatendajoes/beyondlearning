from deps.vision import VideoCapture
from deps.metrics import Metrics

class App:
    def __init__(self, src, show=False):
        self.video_capture = VideoCapture(src)
        self.metrics  = Metrics()
        self.show= show
        self.stopped=False
    
    def stop(self):
        if not self.stopped:
            self.stopped = True
    def run(self):
#Get user input for classid, classdate, classtime, classattendance
        '''classid = input("Enter class ID: ")
        classdate = input("Enter class date (YYYY-MM-DD): ")
        classtime = input("Enter class time (HH:MM): ")
        classattendance = input("Enter class attendance: ")
        # Create a header dictionary with user input
        header = {'classid': classid,
                    'classdate': classdate,
                    'classtime': classtime,
                    'classattendance': classattendance}  # Use 0 for webcam or provide a video file path'''
        while True:
            ret, frame = self.video_capture.read()
            if not ret or self.stopped:
                break
            processed_frame = self.video_capture.process_frame(frame)
            if self.show:
                frame_count = self.video_capture.show(processed_frame)
            if self.video_capture.wait():
                break
        #self.video_capture.release()
        self.video_capture.stop()
        # Metrics calculation and display
        self.metrics.get_buffer(self.video_capture.buffer)
        #self.metrics.dump_metrics(header=head)
        self.metrics.display_metrics()
        self.metrics.plot_metrics()
        
if __name__ == "__main__":
    app = App(src=r'testvideos\rec1.mp4', show=True) 
    #app = App(src=0, show=True) 
    app.run()