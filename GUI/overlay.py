import tkinter as tk
from detect_one import get_prediction
from screenshot_dxcam import shot
import time
from matplotlib import pyplot as plt


class GameOverlay:
    def __init__(self, master):
        self.master = master
        master.title("Game Overlay")

        # Create a label for displaying information
        # self.label = tk.Label(master, text="Overlay Text", font=("Helvetica", 16))
        # self.label.pack(pady=20)

        # Create a canvas for drawing the box
        self.canvas = tk.Canvas(
            master,
            width=1920,
            height=1080,
            bg="white",
            borderwidth=0,
            highlightthickness=0,
        )  # Set canvas size to 1920x1080 and background color to white
        self.canvas.pack()

        # Initialize box coordinates
        self.box_size = 30
        self.box_x = 0
        self.box_y = 0

        # Bind the mouse motion event to the function

        # Draw the initial box
        self.draw_box()

    def draw_box(self):
        # Update box coordinates based on mouse position

        # Draw the updated box
        self.canvas.delete("all")
        img = shot((0, 0, 1920, 1080))

        boxes = get_prediction(img)[0].boxes

        for box in boxes:
            x1, y1 = [int(x) for x in box.xyxy[0][:2]]
            x2, y2 = [int(x) for x in box.xyxy[0][2:]]
            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="white",
                outline="red",
                width=4,
            )

        self.canvas.after(1, self.draw_box)


def create_overlay():
    root = tk.Tk()
    overlay = GameOverlay(root)
    root.attributes("-fullscreen", True)  # Set the window to fullscreen
    root.attributes("-topmost", True)  # Set the window to always be on top
    root.wm_attributes("-transparentcolor", "white")  # Set the background to white
    root.overrideredirect(True)
    return root, overlay


if __name__ == "__main__":
    root, overlay = create_overlay()
    root.mainloop()
