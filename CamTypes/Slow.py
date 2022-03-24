import cv2
import numpy as np
import copy
from .CameraTypes import *

defaults = {"frames" : 10,
            }


class Camera(CameraType):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs, default = defaults)

        ret, frame = this.cameraSource.read()
        this.scale = this.windowSize[:2] / frame.shape[:2]
        this.scale = min(this.scale)

        this.offset = this.windowSize[:2] - np.array(frame.shape[:2]) * this.scale
        this.offset = (this.offset / 2).astype(int)

        frame = cv2.resize(frame, (0, 0), fx = this.scale, fy = this.scale)
        this.framecount = 1
        this.old, this.new = frame, frame


    def getFrame(this):
        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.scale, fy = this.scale)
        #always probe webcam to act as sync

        this.framecount += 1
        if this.framecount > this.frames:
            this.framecount = 1
            this.old = this.new
            this.new = frame

        frame = this.getTween()

        image = np.zeros(this.windowSize, np.uint8)
        image[:] = (0, 255, 0)

        image[this.offset[0] : this.offset[0] + frame.shape[0],
              this.offset[1] : this.offset[1] + frame.shape[1]] = frame

        return image


    def getTween(this):
        p = this.framecount / this.frames
        w = np.zeros(this.old.shape)
        w[:] = p
        n = np.zeros(this.old.shape)
        n[:] = 1 - p
        w = np.array([n, w])
        out = np.average(np.array([this.old, this.new]), axis = 0, weights = w)
        return out


