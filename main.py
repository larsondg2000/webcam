import glob
import cv2
import time
from emailing import send_email, clean_folder
from threading import Thread

# Video capture "cv2.CAP_DSHOW" starts camera quicker
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
time.sleep(1)

first_frame = None
status_list = []
count = 1


while True:
    status = 0
    # Reads the frames
    check, frame = video.read()

    # Covert to Gray and add Gaussian Blur
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # capture first frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # Compare to first frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # threshold is 30, set the white (255), algorythm, second item in lest
    thresh_frame = cv2.threshold(delta_frame,  35, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Displays image
    # cv2.imshow("My Video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # creates green rectangle around new object
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1

            # Store images in images/ folder
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1

            # get list of all images
            all_images = glob.glob("images/*.png")
            # get middle image to send
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    # creates status list 0-> no new object 1-> new object
    status_list.append(status)
    # get last two items of list
    status_list = status_list[-2:]
    # print(status_list)

    # checks status list-> when list goes from [1,1] to [1,0] items leaves frame
    if status_list[0] == 1 and status_list[1] == 0:
        # setup thread for email
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True

        # email thread call
        email_thread.start()

    cv2.imshow("Video", frame)

    # lets you quit by pressing "q"
    key = cv2.waitKey(1)

    if key == ord("q"):
        break


video.release()
