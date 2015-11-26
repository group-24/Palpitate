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

class FaceTracker(object):
    """wrapper around the haarcascades of opencv,
     smooths the video and returns the pixels the desired region"""
    def __init__(self, path_to_opencv_cascades, gui=True, defaults=SUBJECT_ANALYSIS_DEFAULTS):
        self.steadyX = defaults['steadyX']
        self.steadyY = defaults['steadyY']
        self.steadyWidth = defaults['steadyWidth']
        self.steadyHeight = defaults['steadyHeight']
        self.alpha_movement = defaults['alpha_movement']
        self.alpha_face_size = defaults['alpha_face_size']

        self.face_cascade = cv2.CascadeClassifier(path_to_opencv_cascades + 'haarcascade_frontalface_alt2.xml')
        self.eye_cascade = cv2.CascadeClassifier(path_to_opencv_cascades + 'haarcascade_eye.xml')

        self.gui = gui

    def detect_face(self, frame):
        # so there aren't as many selfs around the place
        steadyX = self.steadyX
        steadyY = self.steadyY
        steadyHeight = self.steadyHeight
        steadyWidth = self.steadyWidth
        alpha_movement = self.alpha_movement
        alpha_face_size = self.alpha_face_size

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 1:
            print('more than one face detected')
        elif len(faces) == 0:
            print('no faces detected')
        else:
            (x, y, w, h) = faces[0]
            (steadyX, steadyY) = (
                int(alpha_movement*steadyX + (1-alpha_movement)*x),
                int(alpha_movement*steadyY + (1-alpha_movement)*y)
            )

            (steadyWidth, steadyHeight) = (
                int(alpha_face_size*steadyWidth + (1-alpha_face_size)*w),
                int(alpha_face_size*steadyHeight + (1-alpha_face_size)*h)
            )

            # params for setecting the face

            half_width = (steadyWidth // 2)
            half_height = (steadyHeight // 2)

            center_x = steadyX + half_width
            center_y = steadyY + half_height

            from_middleX = 0.6
            from_middleY = 0.7

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

            # just get the green color
            interesting_pixels = frame[top_right[1]:bottom_left[1], top_right[0]:bottom_left[0]]
            return interesting_pixels

        return None
