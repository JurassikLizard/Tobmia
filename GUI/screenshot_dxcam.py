import dxcam
from PIL import Image

camera = dxcam.create()


def shot(region=(810, 390, 1110, 690)):
    return camera.grab(region)


# benchmarking fps (much faster than mss)
if __name__ == "__main__":
    import time

    l = []
    for x in range(100):
        t = time.time()
        shot()
        l.append(time.time() - t)
    print(sum(l) / len(l))
