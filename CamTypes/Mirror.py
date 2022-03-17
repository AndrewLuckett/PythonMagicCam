import cv2
import numpy as np
import copy
from .CameraTypes import *

defaults = {"vert" : True,
            "preMirror" : False,
            }


class Camera(CameraType):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this.__dict__.update(copy.deepcopy(defaults))
        this.__dict__.update(kwargs)

        ret, frame = this.cameraSource.read()
        this.scale = this.windowSize[:2] / frame.shape[:2]
        this.scale = min(this.scale)

        this.offset = this.windowSize[:2] - np.array(frame.shape[:2]) * this.scale
        this.offset = (this.offset / 2).astype(int)

        frame = cv2.resize(frame, (0, 0), fx = this.scale, fy = this.scale)
        this.trunc = (frame.shape[0] // 2, frame.shape[1])
        if not this.vert:
            this.trunc = (frame.shape[0], frame.shape[1] // 2)


    def getFrame(this):
        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.scale, fy = this.scale)

        if this.preMirror:
            frame = cv2.flip(frame, 1)

        image = np.zeros(this.windowSize, np.uint8)
        image[:] = (0, 255, 0)

        frame = frame[:this.trunc[0], :this.trunc[1]]

        image[this.offset[0] : this.offset[0] + frame.shape[0],
              this.offset[1] : this.offset[1] + frame.shape[1]] = frame

        frame = cv2.flip(frame, 0 if this.vert else 1)

        shift = (frame.shape[0] * this.vert, frame.shape[1] * (not this.vert))

        image[this.offset[0] + shift[0] : this.offset[0] + shift[0] + frame.shape[0],
              this.offset[1] + shift[1] : this.offset[1] + shift[1] + frame.shape[1]] = frame

        return image


