import cv2
import numpy as np
from CamTypes import *
from KeyMap import *
import Optionsmenu

camNum = 0 # Keep at zero unless you have multiple valid cameras
outputSize = np.array([720, 1280, 3])


def main():
    vidSrc = cv2.VideoCapture(camNum)
    assert validateSrc(vidSrc)

    mainloop(vidSrc)

    vidSrc.release()
    cv2.destroyAllWindows()


def mainloop(vidSrc):
    global cam
    cam = CamContainer(vidSrc, outputSize)
    cam.changeCam(Full.Camera)
    while True:
        frame = cam.getFrame()
        cv2.imshow('Python Magic Cam', frame)

        keydown = chr(cv2.waitKey(1) & 0xFF)

        if keydown == chr(27): # Esc to close
            Optionsmenu.closeMenu()
            break

        if keydown == chr(96): # ¬ Key under esc
            Optionsmenu.openMenu(keymap, cam)

        if keydown in keymap.keys():
            cam.changeCam(keymap[keydown].Camera)


def validateSrc(vidSrc):
    frame = None
    try:
        ret, frame = vidSrc.read()
    except:
        return False

    return frame is not None


class CamContainer:
    def __init__(this, vidSrc, outputSize):
        this.vidSrc = vidSrc
        this.outputSize = outputSize

    def getFrame(this):
        return this.cam.getFrame()

    def changeCam(this, cam, **kwargs):
        this.cam = cam(this.vidSrc, this.outputSize, **kwargs)


if __name__ == "__main__":
    main()

