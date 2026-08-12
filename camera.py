import numpy as np
import cv2 as cv
import time
import math

camera = 1
start = time.time()
cap = cv.VideoCapture(camera)

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

elapsed_time = time.time()-start
w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

print(f'Initializing camera {camera} took {elapsed_time:.2f} seconds')
print(f'Frame size = ({h} ,{w})')

count = 0
start = time.time()
sigma = 0

while True:

    count+=1

    ok, img = cap.read()
    if not ok:
        print('Error reading image')
        break

    cv.imshow('Image',img)
        
    k = cv.waitKey(1) # if character 'q' is pressed, exit
    if k == ord('q'):
        break
        

        
elapsed_time = time.time()-start
gcd = math.gcd(img.shape[0], img.shape[1])
print(f'Image shape: {img.shape}')
print(f'Aspect ratio: {img.shape[0]//gcd}/{img.shape[1]//gcd}')
print(f'Captured {count} frames')
print(f'Capture speed: {count/elapsed_time:.2f} frames per second')
cap.release()
cv.destroyAllWindows()
