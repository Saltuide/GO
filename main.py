import os
import sys

import pygame

from tkinter import *
from tkinter import scrolledtext


WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

def done():
    global run
    run = False


class Game:
    def __init__(self):
        self.width = 1200
        self.height = 800
        self.black_points = 0
        self.white_points = 0
        ######################################
        self.root = Tk()
        self.root.title("Go")
        self.root.iconbitmap('icon.ico')
        self.root.configure(bg = 'red')

        embed = Frame(self.root, width=self.width - 330, height=self.height)
        embed.pack(side = LEFT)

        history_win_color = '#%02x%02x%02x' % GRAY #i dunno why it works so weird

        self.history_text = scrolledtext.ScrolledText(self.root , width = 30, height = 30)
        self.history_text.config(state = DISABLED, font = ("Times New Roman", "14", "bold")) # readonly
        self.history_text.pack(pady = 20)

        pass_button = Button(self.root, text = "Pass", height = 2, width = 10)
        pass_button.config(command = self.skip_turn, font= ("Times New Roman", "16", "bold"))
        pass_button.pack()

        self.root.resizable(width=False, height=False)
        
        # Tell pygame's SDL window which window ID to use
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        
        # Show the window so it's assigned an ID.
        self.root.update()
        self.root.protocol("WM_DELETE_WINDOW", done)

        pygame.init()
        self.win = pygame.display.set_mode((self.width - 330, self.height))

        self.coords = {} #паре координат будет соотвествовать пара индексов матрицы
        self.block_size = 40
        self.whos_turn = True #ход черного
        self.menubar()

        self.myfont = pygame.font.SysFont("Times New Roman", 15, "bold")
        label = self.myfont.render("Черные: 0    Белые: 0", 1, (0,0,0))
        self.win.blit(label, (680, 30))

        self.draw_base_field(14, 14)

    def skip_turn(self):
        print("skipped")

    def menubar(self):
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label = "New", command = self.donothing)
        filemenu.add_command(label = "Open", command = self.donothing)
        filemenu.add_command(label = "Save", command = self.donothing)
        filemenu.add_command(label = "Replay", command = self.donothing)
        #filemenu.add_command(label="Save as...", command=self.donothing)
        #filemenu.add_command(label="Close", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = done)
        menubar.add_cascade(label = "Game", menu = filemenu)

        editmenu = Menu(menubar, tearoff = 0)
        # editmenu.add_command(label = "Undo", command = self.donothing)
        # editmenu.add_separator()
        # editmenu.add_command(label = "Cut", command = self.donothing)
        # editmenu.add_command(label = "Copy", command = self.donothing)
        # editmenu.add_command(label = "Paste", command = self.donothing)
        # editmenu.add_command(label = "Delete", command = self.donothing)
        # editmenu.add_command(label = "Select All", command = self.donothing)
        sizemenu = Menu(editmenu, tearoff = 0)
        sizemenu.add_command(label = "9x9", command = lambda: self.draw_base_field(8, 8))
        sizemenu.add_command(label = "11x11", command = lambda: self.draw_base_field(10, 10))
        sizemenu.add_command(label = "13x13", command = lambda: self.draw_base_field(12, 12))
        sizemenu.add_command(label = "15x15", command = lambda: self.draw_base_field(14, 14))
        sizemenu.add_command(label = "17x19", command = lambda: self.draw_base_field(16, 18))
        sizemenu.add_command(label = "11x19", command = lambda: self.draw_base_field(10, 18))

        editmenu.add_cascade(label = "Change size", menu = sizemenu)

        menubar.add_cascade(label = "Edit", menu = editmenu)
        # helpmenu = Menu(menubar, tearoff=0)
        # helpmenu.add_command(label="Help Index", command=self.donothing)
        # helpmenu.add_command(label="About...", command=self.donothing)
        # menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu = menubar)

    def donothing(self):
        print("kappa")

    def draw_base_field(self, x, y):
        self.coords = {}
        field_width = x 
        field_height = y
        up_space = 20
        left_space = 20

        main_surf = pygame.Surface((self.width - 330, self.height))
        main_surf.fill(GRAY)
        self.win.blit(main_surf, (0, 0))
       

        self.game_surf = pygame.Surface((self.block_size * field_width,
                                    self.block_size * field_height))
        self.game_surf.fill(WHITE)

        self.win.blit(self.game_surf, (up_space, left_space))

        label = self.myfont.render("Черные: 0    Белые: 0", 1, (0,0,0))
        self.win.blit(label, (680, 30))

        for x in range(field_width + 1):
            for y in range(field_height + 1):
                block_coord_x = left_space + x * self.block_size
                block_coord_y = up_space + y * self.block_size
                self.coords[(block_coord_x, block_coord_y)] = (x, y)
                if(x == field_width or y == field_height):
                    continue
                rect = pygame.Rect(block_coord_x, block_coord_y,
                                    self.block_size, self.block_size)
                pygame.draw.rect(self.win, BLACK, rect, 1)

        pygame.display.update()

    def add_turn_info(self, x, y):
        self.history_text.config(state = NORMAL)
        if self.whos_turn:
            self.history_text.insert(INSERT, f"Черные сделали ход в {x}:{y}\n")
        else:
            self.history_text.insert(INSERT, f"Белые сделали ход в {x}:{y}\n")
        self.history_text.config(state = DISABLED)

    def place_stones(self, x, y):
        field_size_x, field_size_y = self.game_surf.get_size()
        if x < 20 or y < 20 or x > field_size_x + 20 or y > field_size_y + 20: #выход за граница поля
            print("out of field")
            return
        else:
            tmp_x = round((x - 20) / self.block_size) #смотрим к какому пересечению мы ближе
            tmp_y = round((y - 20) / self.block_size)

            self.add_turn_info(tmp_x, tmp_y)

            tmp_x = 20 + self.block_size * tmp_x #вычисляем координаты этого пересечения
            tmp_y = 20 + self.block_size * tmp_y

            #if(не занято) жду класс Даши
            if self.whos_turn: #ход черных
                pygame.draw.circle(self.win, (255, 0, 0), (tmp_x, tmp_y), 17)
            else:
                pygame.draw.circle(self.win, (0, 0, 255), (tmp_x, tmp_y), 17)

            self.whos_turn = not self.whos_turn
            pygame.display.update()

    


    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.place_stones(event.pos[0], event.pos[1])
  
        pygame.display.update()  
        self.root.update_idletasks()
        self.root.update()


if __name__ == "__main__":         
    game = Game()
    run = True
    while run:
        game.run()

    pygame.quit()




