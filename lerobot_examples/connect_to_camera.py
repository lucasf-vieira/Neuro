import cv2


camera = cv2.VideoCapture(2)

if not camera.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ok, frame = camera.read()
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break