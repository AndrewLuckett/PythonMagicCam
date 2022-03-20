import cv2
import numpy as np
import copy
from .CameraTypes import *

defaults = {"camScale" : 0.5,
            "horibounds" : (1, 10),
            "bouncybounds" : (1.0, 0.4),
            "inbetweens": 0,
            }


class Camera(CameraType):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this.__dict__.update(copy.deepcopy(defaults))
        this.__dict__.update(kwargs)

        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.camScale, fy = this.camScale)
        bounds = this.windowSize - frame.shape

        this.image = np.zeros(this.windowSize, np.uint8)
        this.image[:] = (0, 255, 0)

        this.bouncy = Bouncy(bounds, this.horibounds, this.bouncybounds)


    def getFrame(this):
        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.camScale, fy = this.camScale)

        tweens = this.inbetweens + 1
        for i in range(tweens):
            this.bouncy.update(1 / tweens)
            offset = this.bouncy.getOffset().astype(int)

            this.image[offset[0] : offset[0] + frame.shape[0],
                       offset[1] : offset[1] + frame.shape[1]] = frame

        return this.image


class Bouncy:
    def __init__(this, bounds, horibounds, bouncybounds):
        this.bounds = bounds
        horibounds = np.sort(horibounds)
        this.horimin = horibounds[0]
        this.horidelta = horibounds[1] - horibounds[0]

        bouncybounds = np.sort(bouncybounds)
        this.bouncymin = bouncybounds[0]
        this.bouncydelta = bouncybounds[1] - bouncybounds[0]

        this.pickNew()


    def pickNew(this):
        r = np.random.rand()
        this.offset = np.array([0.0, r * this.bounds[1]])

        angle = 1
        if r > 0.5:
            angle = -1

        r = np.random.rand()
        horivelo = this.horimin + r * this.horidelta
        this.velo = np.array([0.0, angle * horivelo])
        this.bounce = this.bouncymin + (1 - r) * this.bouncydelta


    def update(this, percent = 1):
        if this.offset[0] == this.bounds[0]:
            this.velo[0] *= -this.bounce
        this.velo[0] += percent
        this.offset += this.velo * percent

        if this.offset[0] > this.bounds[0]:
            this.offset[0] = this.bounds[0]

        if this.offset[1] < 0 or this.offset[1] > this.bounds[1]:
            this.pickNew()


    def getOffset(this):
        return this.offset

