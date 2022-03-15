import cv2
import numpy as np
import copy
from .CameraTypes import *

defaults = {}

class FullCam(CameraType):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this.__dict__.update(copy.deepcopy(defaults))
        this.__dict__.update(kwargs)

        ret, frame = this.cameraSource.read()
        this.scale = this.windowSize[:2] / frame.shape[:2]
        this.scale = min(this.scale)

        this.offset = this.windowSize[:2] - np.array(frame.shape[:2]) * this.scale
        this.offset = (this.offset / 2).astype(int)


    def getFrame(this):
        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.scale, fy = this.scale)

        image = np.zeros(this.windowSize, np.uint8)
        image[:] = (0, 255, 0)

        image[this.offset[0] : this.offset[0] + frame.shape[0],
              this.offset[1] : this.offset[1] + frame.shape[1]] = frame

        return image

