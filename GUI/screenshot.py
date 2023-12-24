import mss, numpy as np


def shot(monitor={"top": 0, "left": 0, "width": 1920, "height": 1080}):
    with mss.mss() as sct:
        # The screen part to capture

        # Grab the data
        sct_img = np.array(sct.grab(monitor))
        return sct_img
        # Save to the picture file
