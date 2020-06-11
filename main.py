import os
import sys

import pygame
from tkinter import *


def done():
    global run
    run = False

class Game:
    def __init__(self):
        self.white = (255, 255, 255)
        self.gray = (200, 200, 200)
        self.black = (0, 0, 0)
        self.width = 1200
        self.height = 900
        ######################################
        self.root = Tk()
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_command(label="Save as...", command=self.donothing)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

        embed = Frame(self.root, width=self.width, height=self.height)
        embed.pack()
        self.root.resizable(width=False, height=False)
        
        

        # Tell pygame's SDL window which window ID to use
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        # Show the window so it's assigned an ID.
        self.root.update()
        self.root.protocol("WM_DELETE_WINDOW", done)

        pygame.init()
        
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ГО")
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)
        self.coords = {} #паре координат будет соотвествовать пара индексов матрицы
        self.block_size = 40
        self.whos_turn = True #ход черного
        self.draw_base_field()


    def donothing(self):
        print("kappa")


    def draw_base_field(self):
        #self.block_size = 40 #Set the size of the grid block
        field_width = field_height = 14
        up_space = 20
        left_space = 20

        main_surf = pygame.Surface((self.width, self.height))
        main_surf.fill(self.gray)
        self.win.blit(main_surf, (0, 0))

        self.game_surf = pygame.Surface((self.block_size * field_width,
                                    self.block_size * field_height))
        self.game_surf.fill(self.white)
        self.win.blit(self.game_surf, (up_space, left_space))

        for x in range(field_width + 1):
            for y in range(field_height + 1):
                block_coord_x = left_space + x * self.block_size
                block_coord_y = up_space + y * self.block_size
                self.coords[(block_coord_x, block_coord_y)] = (x, y)
                if(x == field_width or y == field_height):
                    continue
                rect = pygame.Rect(block_coord_x, block_coord_y,
                                    self.block_size, self.block_size)
                pygame.draw.rect(self.win, self.black, rect, 1)

        pygame.display.update()

    def place_stones(self, x, y):
        field_size_x, field_size_y = self.game_surf.get_size()
        if x < 20 or y < 20 or x > field_size_x + 20 or y > field_size_y + 20: #выход за граница поля
            print("out of field")
            return
        else:
            tmp_x = round((x - 20) / self.block_size) #смотрим к какому пересечению мы ближе
            tmp_y = round((y - 20) / self.block_size)

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
        #run = True
        

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.place_stones(event.pos[0], event.pos[1])
        #while run:
            # def done():
            #     global run
            #     run = False
            
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         run = False
            #     elif event.type == pygame.MOUSEBUTTONDOWN:
            #         self.place_stones(event.pos[0], event.pos[1])
        pygame.display.update()  # (or pygame.display.update())
        self.root.update_idletasks()
        self.root.update()
            #pygame.time.wait(1000)

            
        # pygame.quit()
        # sys.exit()


game = Game()

run = True
while run:
    game.run()

pygame.quit()




