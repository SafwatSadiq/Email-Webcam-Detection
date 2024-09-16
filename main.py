import cv2
import time
from emailing import send_email
import glob
import os

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

video.set(cv2.CAP_PROP_FRAME_WIDTH, 1066)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    images = glob.glob("image/*.png")
    for image in images:
        os.remove(image)


while video.isOpened():
    status = 0
    check ,frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (11, 11), 0)
    
    if first_frame is None:
        first_frame = gray_frame_gau
        cv2.imwrite("image.png", gray_frame_gau)
    
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dile_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imwrite("image.png", dile_frame)
    
    contours, check = cv2.findContours(dile_frame, cv2.RECURS_FILTER, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y) , (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"Image/{count}.png", frame)
            count += 1
            
    status_list.append(status)
    status_list = status_list[-2:]
    
    if status_list[0] == 1 and status_list[1] == 0:
        all_images = glob.glob("Image/*.png")
        index = int(len(all_images) / 2)
        image_with_obj = all_images[index]
        send_email(image_with_obj)
        clean_folder()
    
    cv2.imshow('My Video', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()