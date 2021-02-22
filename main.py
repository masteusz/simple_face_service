import cv2
from mtcnn.mtcnn import MTCNN

if __name__ == "__main__":
    cv2.namedWindow("window")
    cv2.moveWindow("window", 20, 20)
    detector = MTCNN()
    cap = cv2.VideoCapture(2)
    cnt = 0
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        detected = detector.detect_faces(frame)
        print(detected)
        if detected:
            for face in detected:
                x1, y1, width, height = face.get("box")
                right_eye = face.get("keypoints").get("right_eye")
                left_eye = face.get("keypoints").get("left_eye")
                nose = face.get("keypoints").get("nose")
                mouth_left = face.get("keypoints").get("mouth_left")
                mouth_right = face.get("keypoints").get("mouth_right")
                cv2.rectangle(frame, (x1, y1), (x1 + width, y1 + height), (0, 255, 0))
                cv2.circle(frame, left_eye, 3, (0, 255, 0))
                cv2.circle(frame, right_eye, 3, (0, 255, 0))
                cv2.circle(frame, nose, 3, (0, 255, 0))
                cv2.line(frame, mouth_left, mouth_right, (0, 255, 0))

        cv2.imshow("window", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
