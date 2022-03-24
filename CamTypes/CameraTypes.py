import copy

class CameraType:
    def __init__(this, cameraSource, windowSize, default = {}, *args, **kwargs):
        this.cameraSource = cameraSource
        this.windowSize = windowSize

        this.__dict__.update(copy.deepcopy(default))
        this.__dict__.update(kwargs)


    def getFrame(this):
        return None

