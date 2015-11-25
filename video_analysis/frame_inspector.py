TIME_SECOND_WINDOW = 4


class frame_inspector(object):
    """This class inspects the frame of a video, then produces spectrograms of the
    desired features of the frame"""

    def __init__(self, heartrates, frame_rate):
        self.heartrates = heartrates
        self.frame_rate = frame_rate
        self.frames_processed = 0

    def extract(self, img, (x, y, width, height)):
        half_width = (steadyWidth // 2)
        half_height = (steadyHeight // 2)

        center_x = steadyX + half_width
        center_y = steadyY + half_height

        # the amounts from the middle of the face that we extend the square to
        # get the interesting_pixels
        from_middleX = 0.6
        from_middleY = 0.8

        # top right and bottom left of the square
        top_right = (
            steadyX + int((1-from_middleX) * half_width),
            center_y
        )

        bottom_left = (
            center_x + int(half_width * from_middleX),
            center_y + int(half_height * from_middleY)
        )

        # just get the green color
        interesting_pixels = frame[top_right[1]:bottom_left[1], top_right[0]:bottom_left[0], 1]
        # self.pixels = 

        if self.frames_processed = (self.frame_rate * TIME_SECOND_WINDOW):
            # make the spectrograms
        else:
            self.frames_processed += 1



    def lost_frame(self):
        throw Error("NOT DONE YET")

    def
