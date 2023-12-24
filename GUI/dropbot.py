import requests, tkinter as tk

# pyautogui.mouseInfo()
# exit()


class info:
    def __init__(self):
        self.busStartX = 0
        self.busStartY = 0
        self.busStopX = 0
        self.busStopY = 0
        self.targetx = 0
        self.targety = 0


# 750x750+580+200
def drop_ui():
    map_info = info()

    root = tk.Tk()
    root.overrideredirect(False)
    # root.geometry("750x750+580+200")
    width, height = 1920, 1080

    offsetx, offsety = 580, 200
    root.wm_attributes("-fullscreen", True)
    root.wm_attributes("-topmost", True)
    root.lift()

    # root.wm_attributes("-transparentcolor", "red")
    root.attributes("-alpha", 0.1)

    canvas = tk.Canvas(
        root, width=width, height=height, bg="white", highlightthickness=0
    )
    canvas.pack()
    canvas.focus_set()
    length = 5

    def press(key):
        x, y = int((key.x - offsetx) * 2 / 3), int((key.y - offsety) * 2 / 3)
        if key.keysym == "Tab":
            print("quitting")
            root.destroy()
        elif key.keysym == "1":
            map_info.busStartX, map_info.busStartY = x, y
            print("Bus start set to", map_info.busStartX, map_info.busStartY)
        elif key.keysym == "2":
            map_info.busStopX, map_info.busStopY = x, y
            print("Bus stop set to", map_info.busStopX, map_info.busStopY)
        elif key.keysym == "3":
            map_info.targetx, map_info.targety = x, y
            print("Target set to", map_info.targetx, map_info.targety)
            jumpx, jumpy, glidex, glidey = get_coords(map_info)
            print(jumpx, jumpy, glidex, glidey)
            canvas.create_oval(
                jumpx - length + offsetx,
                jumpy - length + offsety,
                jumpx + length + offsetx,
                jumpy + length + offsety,
                fill="red",
            )
            # canvas.create_oval(
            #     glidex - length + offsetx,
            #     glidey - length + offsety,
            #     glidex + length + offsetx,
            #     glidey + length + offsety,
            #     fill="blue",
            # )
            canvas.create_line(
                jumpx + offsetx,
                jumpy + offsety,
                glidex + offsetx,
                glidey + offsety,
                fill="black",
                width=2,
            )
            root.attributes("-alpha", 1)
            root.wm_attributes("-transparentcolor", "white")

    def get_coords(object: info):
        r = requests.get(
            f"https://www.landingtutorial.com/ajax/preanalyze.php?targetX={object.targetx}&targetY={object.targety}&busStartX={object.busStartX}&busStartY={object.busStartY}&busStopX={object.busStopX}&busStopY={object.busStopY}"
        )

        response = list(
            map(
                lambda x: int(float(x) * 750),
                r.text[5:-10].split(","),
            )
        )

        return response

    print("starting")
    root.bind("<Key>", press)
    root.mainloop()


if __name__ == "__main__":
    drop_ui()
