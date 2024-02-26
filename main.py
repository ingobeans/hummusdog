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
        self.pixels = [[{"char":" ","foreground_color":(255,255,255),"background_color":(0,0,0)} for _ in range(width)] for _ in range(height)]
        self.reload()

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
        self.pixels[y][x] = color

    def draw_string(self, x, y, color, text):
        for char_y in range(len(text.split("\n"))):
            for char_x in range(len(text.split("\n")[char_y])):
                self.pixels[y+char_y][x+char_x]["char"] = text.split("\n")[y][x]
                self.pixels[y+char_y][x+char_x]["foreground_color"] = color
    
    def draw_circle(self, x, y, color, width):
        pass

if __name__ == "__main__":
    program = Hummusdog(75,14)
    program.draw_string(0,0,(255,0,255),"hello")
    program.reload()