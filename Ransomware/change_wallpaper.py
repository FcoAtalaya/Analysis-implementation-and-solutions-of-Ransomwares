import ctypes
from PIL import Image
import os
import cv2
import requests

def getImage(url):
    with open('base.jpg', 'wb') as f:
        f.write(requests.get(url+'/image').content)
    f.close()

def makeWallpaper(im1,im2):
    area = (200, 0, 500, 400)
    cropped_img = im2.crop(area)

    back_im = im1.copy()
    back_im.paste(cropped_img, (100, 10))
    back_im.save('wallpaper.png', quality=100)

def changeWallpaper(url):
    
    getImage(url)

    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    if cam is not None and cam.isOpened():

        result, image = cam.read()
        cv2.imwrite("photo.jpg", image)

        im1 = Image.open(os.getcwd()+r'\base.jpg')
        im2 = Image.open(os.getcwd()+r'\photo.jpg')

        makeWallpaper(im1,im2)
        os.remove("photo.jpg")
        
        path = os.getcwd() + r'\wallpaper.png'
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        os.remove("wallpaper.png")
    else:
        path = os.getcwd() + r'\base.jpg'
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
    os.remove('base.jpg')