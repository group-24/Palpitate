from data_analysis.heart_rate_generator import HeartRateGenerator
from server.heart_rate_imposer import HeartRateImposer
import sys

if __name__ == "__main__":
    video_file = sys.argv[1]
    opencv_path = sys.argv[2]

    hri = HeartRateImposer(video_file, opencv_path)
    hri.pipe_heartrate_frames()

