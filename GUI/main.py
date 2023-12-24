import PySimpleGUI as sg
from screeninfo import get_monitors
import dropbot


# Sensitivity, Screen Size, Strength, toggle aimbot,
def get_screen_resolution():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height


SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_resolution()
print(f"Screen resolution is {SCREEN_WIDTH}x{SCREEN_HEIGHT}")

layout = [
    [
        [
            sg.Text("Sensitivity"),
            sg.InputText("10.0", size=(5, 1), key="-SENSITIVITY-"),
        ],
        [
            sg.Text("DPI"),
            sg.Slider(
                range=(0, 5000),
                default_value=10,
                resolution=100,
                orientation="horizontal",
                key="-DPI-",
            ),
        ],
        [
            sg.Text("Aimbot Strength"),
            sg.Slider(
                range=(0, 100),
                default_value=50,
                resolution=1,
                orientation="horizontal",
                key="-Strength-",
            ),
        ],
        sg.Button("Toggle Aimbot"),
        sg.Button("Dropbot"),
        sg.Button("Apply"),
        sg.Button("Exit"),
    ],
]

window = sg.Window(
    "Tobmia",
    layout,
    keep_on_top=True,
    location=(100, 100),
    background_color="grey",
    grab_anywhere=True,
)

dpi, strength, sensitivity = 0, 0, 0
on = False
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    if event == "Apply":
        dpi = values["-DPI-"]
        strength = values["-Strength-"]
        sensitivity = values["-SENSITIVITY-"]
        print(dpi, strength, sensitivity)

    if event == "Toggle Aimbot":
        if on == False:
            on = True
            print("Aimbot on")
        else:
            on = False
            print("Aimbot off")

    if event == "Dropbot":
        dropbot.drop_ui()
        print("dropped")
window.close()
