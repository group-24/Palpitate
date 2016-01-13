import cv2

# TODO:
#   deal with when the face is lost and try again

SUBJECT_ANALYSIS_DEFAULTS = {
    'steadyX': 400,
    'steadyY': 185,
    'steadyWidth': 250,
    'steadyHeight': 250,
    'alpha_movement': 0.9,
    'alpha_face_size': 0.9
}
DEFAULT_FAULT_TOLERANCE = 10

class FaceTracker(object):
    """wrapper around the haarcascades of opencv,
     smooths the video and returns the pixels the desired region"""
    def __init__(self, path_to_opencv_cascades, gui=True, defaults=SUBJECT_ANALYSIS_DEFAULTS, fault_tolerance=DEFAULT_FAULT_TOLERANCE):
        self.steadyX = defaults['steadyX']
        self.steadyY = defaults['steadyY']
        self.steadyWidth = defaults['steadyWidth']
        self.steadyHeight = defaults['steadyHeight']
        self.alpha_movement = defaults['alpha_movement']
        self.alpha_face_size = defaults['alpha_face_size']

        self.face_cascade = cv2.CascadeClassifier(path_to_opencv_cascades + 'haarcascade_frontalface_alt2.xml')
        self.eye_cascade = cv2.CascadeClassifier(path_to_opencv_cascades + 'haarcascade_eye.xml')

        self.gui = gui
        self.consecutive_frames_lost = 0
        self.fault_tolerance = fault_tolerance

    def detect_face(self, frame):
        """Called to find a face in the video, if more than """

        # so there aren't as many selfs around the place
        steadyX = self.steadyX
        steadyY = self.steadyY
        steadyHeight = self.steadyHeight
        steadyWidth = self.steadyWidth
        alpha_movement = self.alpha_movement
        alpha_face_size = self.alpha_face_size

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        interesting_pixels = None

        if len(faces) == 1:
            (x, y, w, h) = faces[0]
            (steadyX, steadyY) = (
                int(alpha_movement*steadyX + (1-alpha_movement)*x),
                int(alpha_movement*steadyY + (1-alpha_movement)*y)
            )

            (steadyWidth, steadyHeight) = (
                int(alpha_face_size*steadyWidth + (1-alpha_face_size)*w),
                int(alpha_face_size*steadyHeight + (1-alpha_face_size)*h)
            )

        else:
            # either 0 or more than one face detected
            self.consecutive_frames_lost += 1
            if self.consecutive_frames_lost > self.fault_tolerance:
                raise RuntimeError('Too many consecutive frames dropped to find the face')

        half_width = (steadyWidth // 2)
        half_height = (steadyHeight // 2)

        center_x = steadyX + half_width
        center_y = steadyY + half_height

        from_middleX = 0.6
        from_middleY = 0.3

        top_right = (
            steadyX + int((1-from_middleX) * half_width),
            center_y
        )

        bottom_left = (
            center_x + int(half_width * from_middleX),
            center_y + int(half_height * from_middleY)
        )

        if self.gui:
            # draw a rectangle
            cv2.rectangle(frame, (steadyX, steadyY), (steadyX+steadyWidth, steadyY+steadyHeight), (0, 255, 0), 2)
            cv2.rectangle(frame, top_right, bottom_left, (255, 255, 0), 2)
            cv2.imshow('Palpitate face tracker', frame)

        interesting_pixels = frame[top_right[1]:bottom_left[1], top_right[0]:bottom_left[0]]

        self.steadyX = steadyX
        self.steadyY = steadyY
        self.steadyHeight = steadyHeight
        self.steadyWidth = steadyWidth
        self.alpha_movement = alpha_movement
        self.alpha_face_size = alpha_face_size
        return interesting_pixels
