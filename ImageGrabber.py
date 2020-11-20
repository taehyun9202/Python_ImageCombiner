import keyboard
import time

from PIL import ImageGrab #python image library

time.sleep(5) # start grabbing after 5sec

# for i in range(1, 11):
#     img = ImageGrab.grab()  # screenshot
#     img.save("image{}.png".format(i))
#     time.sleep(2)

def screenshot():
    cur_time = time.strftime("_%m%d%Y_%H%M%S")
    img = ImageGrab.grab()  # screenshot
    img.save("image{}.png".format(cur_time))

keyboard.add_hotkey("`", screenshot)

keyboard.wait("esc")