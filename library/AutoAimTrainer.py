import pyautogui
import time





class AimTrainer:
    last_pos = 0 # Value stored to make sure not clicky same place

    # Finds a color and clicks it, pretty cool
    @classmethod
    def find_color(cl,target_color, step=1, x_offset=0, y_offset=0, interval=0, max_attempts=1, x_min=0, y_min=0, x_max=1920, y_max=1080): # x_max and y_max default values are for a 1080x1920p monitor
        if not target_color: raise ValueError('target_color parameter is required')
        attempts = 0
        while attempts < max_attempts:

            screen = pyautogui.screenshot()
            if x_max > screen.width: raise ValueError('x_max bigger than screen width')
            if y_max > screen.height: raise ValueError('y_max bigger than screen height')
            #Just loops through the region and clicks a color if it finds it then returns
            for x in range(x_min, x_max, step):
                for y in range(y_min, y_max, step):

                    if x+y == cl.last_pos: continue
                    pixel_color = screen.getpixel((x, y))
                    if pixel_color == target_color:
                        pyautogui.click(x + x_offset, y + y_offset)
                        cl.last_pos = (x + x_offset) + (y + y_offset)
                        return
                    
            time.sleep(interval)
            attempts += 1

    # Finds a img and clicks it cuz yes
    @classmethod
    def find_image(cl, image_path, top_left=[0,0], bottom_right=[1920,1080]):
        if not image_path: raise ValueError('image_path parameter is required')
        # Pretty much just use locateCenterOnScreen for this
        image_check = pyautogui.locateCenterOnScreen(image_path,region=(top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
        if image_check is not None:
            x, y = image_check
            pyautogui.click(x, y)

    @classmethod
    def AutoTrainerColor(cl, target_color, x_offset=0, y_offset=0, search_interval=0, top_left=[0,0], bottom_right=[1920,1080]):
        if not target_color: raise ValueError('target_color parameter is required')
        try:
            while True:
                cl.find_color(target_color, x_offset = x_offset, y_offset = y_offset, x_min = top_left[0], y_min = top_left[1], x_max = bottom_right[0], y_max = bottom_right[1])
                time.sleep(search_interval)
        except (KeyboardInterrupt, pyautogui.FailSafeException):
            return False
        
    @classmethod
    def AutoTrainerImage(cl, image_path, search_interval=0, top_left=[0,0], bottom_right=[1920,1080]):
        if not image_path: raise ValueError('image_path parameter is required')
        try:
            while True:
                cl.find_image(image_path, top_left = top_left, bottom_right = bottom_right)
                time.sleep(search_interval)
        except (KeyboardInterrupt, pyautogui.FailSafeException):
            return False




