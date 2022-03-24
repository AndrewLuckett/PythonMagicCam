import cv2
import numpy as np

from .CameraTypes import *

defaults = {"camScale" : 0.75,
            "randomStart" : False,
            "count" : 13,
            "veloMin" : 0.5,
            "veloInc" : 0.5,
            }


class Camera(CameraType):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs, default = defaults)

        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.camScale, fy = this.camScale)
        bounds = this.windowSize - frame.shape
        offset = np.array([0.0, 0.0])
        angle = np.array([1, 1])

        if this.randomStart:
            offset = np.random.rand(2) * bounds[:2]
            angle = np.random.choice(2, 2)

        this.bouncy = []
        for i in range(this.count):
            v = this.veloMin + this.veloInc * i
            this.bouncy.append(Bouncy(offset, angle, bounds, v))


    def getFrame(this):
        ret, frame = this.cameraSource.read()
        frame = cv2.resize(frame, (0, 0), fx = this.camScale, fy = this.camScale)

        image = np.zeros(this.windowSize, np.uint8)
        image[:] = (0, 255, 0)

        for b in this.bouncy:
            b.update()
            o = b.getOffset().astype(int)

            image[o[0] : o[0] + frame.shape[0],
                  o[1] : o[1] + frame.shape[1]] = frame

        return image


class Bouncy():
    def __init__(this, start, angle, bounds, velocity):
        this.offset = start.astype(float)
        this.angle = angle.astype(int)
        this.bounds = bounds
        this.velocity = velocity


    def update(this, percent = 1):
        this.offset += this.velocity * percent * (this.angle * 2 - np.array([1, 1]))

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


    def getOffset(this):
        return this.offset

