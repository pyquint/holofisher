import cv2
import mss
import numpy as np
import pydirectinput


with mss.mss() as sct:
    target_rgbs = {"enter": (173, 49, 207),
                   'w': (225, 50, 50), 's': (52, 144, 245),
                   'a': (244, 196, 66), 'd': (45, 234, 43)}
    region = {"top": 725, "left": 1180, "width": 4, "height": 75}

    np_colors = {prompt: np.array(rgb) for (prompt, rgb) in target_rgbs.items()}
    threshold = 10

    while True:
        screenshot = sct.grab(region)
        screenshot_array = np.array(screenshot.pixels, dtype=np.uint8)
        cropped_screenshot = screenshot_array[..., :3]

        for prompt in target_rgbs:
            target_color = np_colors[prompt].astype(cropped_screenshot.dtype)
            diff = np.sum(np.abs(cropped_screenshot - target_color), axis=2)

            if np.any(diff < threshold):
                pydirectinput.press(prompt)

        if sct.grab({"top": 820, "left": 960, "width": 1, "height": 1}).rgb == b"\xf9\xf9\xf9":
            pydirectinput.press('z', 2)
