import cv2
import numpy as np
import copy
from .CameraTypes import *

defaults = {"camScale" : 0.75,
            "rate" : 45,
            }


class Camera(CameraType):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this.__dict__.update(copy.deepcopy(defaults))
        this.__dict__.update(kwargs)

        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.camScale, fy = this.camScale)
        this.bounds = this.windowSize - frame.shape

        this.count = 0

        this.offset = np.random.rand(2) * this.bounds[:2]
        this.offset = this.offset.astype(int)


    def getFrame(this):
        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.camScale, fy = this.camScale)

        image = np.zeros(this.windowSize, np.uint8)
        image[:] = (0, 255, 0)

        this.count += 1

        if this.count > this.rate:
            this.offset = np.random.rand(2) * this.bounds[:2]
            this.offset = this.offset.astype(int)
            this.count = 0

        image[this.offset[0] : this.offset[0] + frame.shape[0],
              this.offset[1] : this.offset[1] + frame.shape[1]] = frame

        return image

