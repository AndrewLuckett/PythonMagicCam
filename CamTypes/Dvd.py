import cv2
import numpy as np
import copy
from .CameraTypes import *

defaults = {"camScale" : 0.75,
            "angle" : np.array([True, True]),
            "velocity" : 1,
            "offset" : np.array([100, 10]),
            "randomStart" : True,
            }


class Camera(CameraType):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this.__dict__.update(copy.deepcopy(defaults))
        this.__dict__.update(kwargs)

        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.camScale, fy = this.camScale)
        this.bounds = this.windowSize - frame.shape

        if this.randomStart:
            this.offset = np.random.rand(2) * this.bounds[:2]
            this.offset = this.offset.astype(int)
            this.angle = np.random.choice(2, 2)


    def getFrame(this):
        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.camScale, fy = this.camScale)

        image = np.zeros(this.windowSize, np.uint8)
        image[:] = (0, 255, 0)

        this.offset += this.velocity * (this.angle * 2 - np.array([1, 1]))

        if this.offset[0] >= this.bounds[0]:
            this.offset[0] = this.bounds[0] * 2 - this.offset[0]
            this.angle[0] = False
        elif this.offset[0] <= 0:
            this.offset[0] = abs(this.offset[0])
            this.angle[0] = True

        if this.offset[1] >= this.bounds[1]:
            this.offset[1] = this.bounds[1] * 2 - this.offset[1]
            this.angle[1] = False
        elif this.offset[1] <= 0:
            this.offset[1] = abs(this.offset[1])
            this.angle[1] = True

        image[this.offset[0] : this.offset[0] + frame.shape[0],
              this.offset[1] : this.offset[1] + frame.shape[1]] = frame

        return image

