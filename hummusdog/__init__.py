import os

if os.name == "nt":
    os.system("color")

def rgb_to_ansi(foreground_rgb: tuple, background_rgb: tuple = None) -> str:
    foreground_code = f"38;2;{foreground_rgb[0]};{foreground_rgb[1]};{foreground_rgb[2]}"
    background_code = f"48;2;{background_rgb[0]};{background_rgb[1]};{background_rgb[2]}" if background_rgb else ""
    
    if background_rgb:
        return f"\x1b[{foreground_code};{background_code}m"
    else:
        return f"\x1b[{foreground_code}m"


reset_color = '\033[0m'

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class Hummusdog:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.clear()
        self.reload()

    def clear(self, color = (0,0,0)):
        self.pixels = [[{"char":" ","foreground_color":(255,255,255),"background_color":color} for _ in range(self.width)] for _ in range(self.height)]

    def get_pixel(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return {"char":" ","foreground_color":(255,255,255),"background_color":(0,0,0), "fake":True}
        return self.pixels[y][x]

    def reload(self):
        clear_terminal()
        last_bg_color = None
        last_fg_color = None
        for y in range(len(self.pixels)):
            for x in range(len(self.pixels[y])):
                background_color = self.pixels[y][x]["background_color"]
                foreground_color = self.pixels[y][x]["foreground_color"]
                char = self.pixels[y][x]["char"]
                if last_bg_color == background_color and last_fg_color == foreground_color:
                    print(char, end="")
                    continue

                print(rgb_to_ansi(foreground_color,background_color) + char, end="")
                last_bg_color = background_color
                last_fg_color = foreground_color

            print()
        print(reset_color,end="",flush=True)

    def set_pixel(self, x, y, color):
        pixel = self.get_pixel(x,y)
        pixel["background_color"] = color
        pixel["char"] = " "

    def draw_string(self, x, y, color, text):
        for char_y in range(len(text.split("\n"))):
            for char_x in range(len(text.split("\n")[char_y])):
                pixel = self.get_pixel(x + char_x, y + char_y)
                pixel["char"] = text.split("\n")[char_y][char_x]
                pixel["foreground_color"] = color
    
    def draw_circle(self, x, y, color, radius_width, radius_height = None, allow_sharp = False)->int:
        """Draw a circle. Radius_width refers to the radius, and if radius_height it specified circle can be oval.
        If allow_sharp is true, it will allow single pixels on a row, which are normally removed since they stick out too much.
        Returns how many pixels were in the circle"""
        
        if not radius_height:
            radius_height = radius_width
        
        amt = 0

        for c_y in range(-radius_height, radius_height + 1):
            pixels = []
            for c_x in range(-radius_width, radius_width + 1):
                pos_x = x + c_x
                pos_y = y + c_y
                
                distance = (c_x / radius_width)**2 + (c_y / radius_height)**2
                if distance <= 1:
                    pixel = self.get_pixel(pos_x, pos_y)
                    pixels.append((pos_x,pos_y,pixel.copy()))
                    amt += 1
                    pixel["background_color"] = color
                    pixel["char"] = " "
            
            if len(pixels) == 1:
                print(pixels)
                pixel = self.get_pixel(pixels[0][0],pixels[0][1])
                print(f"WA: {pixel}")
                pixel["char"] = pixels[0][2]["char"]
                pixel["background_color"] = pixels[0][2]["background_color"]
                
                # if a row has a single square, remove it.
                # since squares are so tall, it looks weird when
                # a single square sticks out vertically.
        return amt
        

if __name__ == "__main__":
    program = Hummusdog(75,14)
    program.draw_string(0,0,(255,0,255),"hello")
    program.draw_circle(12,6,(255,0,0),5,3)
    program.reload()