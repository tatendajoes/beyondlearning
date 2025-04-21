import pandas as pd
import os

class Metrics:
    def __init__(self, buffer={}, header={'classid': None, 'classdate':None, 'classtime':None, 'classattendace':None }):
        self.buffer = buffer
        self.header = header
        self.df = pd.DataFrame(buffer)  # Create DataFrame from buffer
        
    def get_buffer(self, buffer):
        # Load the buffer data into a DataFrame
        self.buffer = buffer
        self.df = pd.DataFrame(buffer)  # Create DataFrame from buffer
    def calculate_metrics(self):
        # Calculate metrics based on the buffer data
        self.df['timestamp'] = self.df['timestamp'].astype(float)
        self.df['confidence'] = self.df['confidence'].astype(float)
        focused_count = (self.df['label'] == 'focused').sum()
        unfocused_count = (self.df['label'] == 'unfocused').sum()
        total_count = len(self.df)
        focused_percentage = (focused_count / total_count) * 100 if total_count > 0 else 0
        unfocused_percentage = (unfocused_count / total_count) * 100 if total_count > 0 else 0

        return {
            'total_frames': total_count,
            'focused_frames': focused_count,
            'unfocused_frames': unfocused_count,
            'focused_percentage': focused_percentage,
            'unfocused_percentage': unfocused_percentage
        }
    def dump_metrics(self, header):
        self.header = header
        filename=fr'dump\metrics{self.header['classid']}.csv'
        filename_header = fr'dump\header\headerlist.csv'
        # Save the metrics to a CSV file
        header_df = pd.DataFrame([header])
        if os.path.exists(filename_header):
            header_df.to_csv(filename_header, index = False, mode= 'a', header=False) # Save the header to a CSV file
        else:
            header_df.to_csv(filename_header, index=False)
        self.df.to_csv(filename, index=False) # Save the DataFrame to a CSV file
        print(f"Metrics saved to {filename}")
        print(f"Header saved to {filename_header}")
        #***ventully use sqlite to save the metrics and header to a database
    def display_metrics(self):
        # Display the metrics in a readable format
        metrics = self.calculate_metrics()
        print("Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value}")
    def plot_metrics(self):
        # Plot the metrics using matplotlib
        import matplotlib.pyplot as plt

        metrics = self.calculate_metrics()
        labels = list(metrics.keys())
        values = list(metrics.values())

        plt.bar(labels, values)
        plt.xlabel('Metrics')
        plt.ylabel('Values')
        plt.title('Metrics Overview')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()