import cv2
import numpy as np
from CamTypes import *

camNum = 0 # Keep at zero unless you have multiple valid cameras
outputSize = np.array([720, 1280, 3])

keymap = {'w' : Full.FullCam,
          'e': Dvd.DvdCam,
          "r": Random.RandomCam
          }


def main():
    vidSrc = cv2.VideoCapture(camNum)
    assert validateSrc(vidSrc)
    
    mainloop(vidSrc)
    
    vidSrc.release()
    cv2.destroyAllWindows()


def mainloop(vidSrc):
    global cam
    cam = Full.FullCam(vidSrc, outputSize)
    while True:
        frame = cam.getFrame()
        cv2.imshow('Python Magic Cam', frame)

        keydown = chr(cv2.waitKey(1) & 0xFF)
        
        if keydown == chr(27): # Esc to close
            break

        if keydown in keymap.keys():
            cam = keymap[keydown](vidSrc, outputSize)


def validateSrc(vidSrc):
    frame = None
    try:
        ret, frame = vidSrc.read()
    except:
        return False

    return frame is not None


if __name__ == "__main__":
    main()
