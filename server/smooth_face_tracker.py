import cv2

ALPHA_MOVEMENT = 0.7
ALPHA_FACE_SIZE = 0.9
FAULT_TOLERANCE = 10 # number of frames lost before it stops

class SmoothFaceTracker(object):
    """Tracks one face smoothly"""
    def __init__(self, opencv_path, alpha_face_size=ALPHA_FACE_SIZE, alpha_movement=ALPHA_MOVEMENT, fault_tolerance=FAULT_TOLERANCE):
        self.alpha_movement = alpha_movement
        self.alpha_face_size = alpha_face_size
        self.fault_tolerance = fault_tolerance

        self.face_cascade = cv2.CascadeClassifier(opencv_path + 'data/haarcascades/haarcascade_frontalface_alt2.xml')

        self.consecutive_frames_lost = 0
        self.face_found = False # Is it already tracking a face

        self.steadyX = 0
        self.steadyY = 0
        self.steadyWidth = 0
        self.steadyHeight = 0


    def detect_face(self, frame):
        """returns the (x, y, width, height) of the face in the video if there is one, None otherwise. Also returns the """

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
            self.consecutive_frames_lost = 0

            if not self.face_found: # we have found a face in this frame
                self.face_found = True
                (steadyX, steadyY, steadyWidth, steadyHeight) = (x, y, w, h)

            else:
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
                self.face_found = False
                return None, None

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

        interesting_pixels = frame[top_right[1]:bottom_left[1], top_right[0]:bottom_left[0]]

        self.steadyX = steadyX
        self.steadyY = steadyY
        self.steadyHeight = steadyHeight
        self.steadyWidth = steadyWidth
        self.alpha_movement = alpha_movement
        self.alpha_face_size = alpha_face_size

        return (steadyX, steadyY, steadyWidth, steadyHeight), interesting_pixels
