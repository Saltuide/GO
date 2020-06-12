import os
import sys

import pygame
from tkinter import *
from tkinter import scrolledtext

from GameGo import GameGo, Turn


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
        self.replay_mode = False
        self.list_for_replay = [] #для последовательного отображения
        self.turn_to_show = 1

        history_win_color = '#%02x%02x%02x' % GRAY #i dunno why it works so weird
        self.root = Tk()
        self.root.title("Go")
        self.root.iconbitmap('icon.ico')
        self.root.configure(bg = history_win_color)

        embed = Frame(self.root, width=self.width - 330, height=self.height)
        embed.pack(side = LEFT)

        

        self.history_text = scrolledtext.ScrolledText(self.root , width = 30, height = 30)
        self.history_text.config(state = DISABLED, font = ("Times New Roman", "14", "bold")) # readonly
        self.history_text.pack(pady = 20)

        self.pass_button = Button(self.root, text = "Pass", height = 2, width = 10)
        self.pass_button.config(command = self.skip_turn, font= ("Times New Roman", "16", "bold"))
        self.pass_button.pack()

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
        self.skipped_turns = 0 #проверка на конец игры
        self.menubar()

        self.myfont = pygame.font.SysFont("Times New Roman", 15, "bold")
        label = self.myfont.render("Черные: 0    Белые: 0", 1, (0,0,0))
        self.win.blit(label, (680, 30))

        self.draw_base_field(14, 14)

    #пропустить ход
    def skip_turn(self):
        self.history_text.config(state = NORMAL)
        if self.whos_turn:
            self.history_text.insert(INSERT, "Красные пропустили ход\n")
        else:
            self.history_text.insert(INSERT, "Синие пропустили ход\n")
        
        player = 1 if self.whos_turn else 2
        game_logic.history.append(Turn(-1, -1, player))
        self.whos_turn = not self.whos_turn
        self.skipped_turns += 1

        if self.skipped_turns >= 2:
            self.history_text.insert(INSERT, "Игра окончена\n")
            res = game_logic.result()
            self.history_text.insert(INSERT, f"Счет: красные - {res[0]}, черные - {res[1]}\n")

        self.history_text.config(state = DISABLED)

    #создание менюбара
    def menubar(self):
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label = "New", command = self.new_game)
        filemenu.add_command(label = "Open", command = self.download)
        filemenu.add_command(label = "Save", command = self.save)
        filemenu.add_command(label = "Replay", command = self.replay)

        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = done)
        menubar.add_cascade(label = "Game", menu = filemenu)

        editmenu = Menu(menubar, tearoff = 0)

        sizemenu = Menu(editmenu, tearoff = 0)
        sizemenu.add_command(label = "9x9", command = lambda: self.change_size(8, 8))
        sizemenu.add_command(label = "11x11", command = lambda: self.change_size(10, 10))
        sizemenu.add_command(label = "13x13", command = lambda: self.change_size(12, 12))
        sizemenu.add_command(label = "15x15", command = lambda: self.change_size(14, 14))
        sizemenu.add_command(label = "17x19", command = lambda: self.change_size(16, 18))
        sizemenu.add_command(label = "11x19", command = lambda: self.change_size(10, 18))

        editmenu.add_cascade(label = "Change size", menu = sizemenu)
        menubar.add_cascade(label = "Edit", menu = editmenu)
        self.root.config(menu = menubar)

    #мгновенное открытие файла
    def download(self):
        try:
            save_file = open('save.txt', 'r')
        except:
            self.history_text.config(state = NORMAL)
            self.history_text.insert(INSERT, "Файл не найден")
            self.history_text.config(state = DISABLED)
            return
        x = 0; y = 0
        history = ""

        lines = save_file.readlines()
   
        for i, line in enumerate(lines):
            if i == 0:
                size = line.split(' ')
                height = int(size[0]); width = int(size[1])
                game_logic.update(height, width)
                self.new_game()
            elif i == len(lines) - 1: #не записываем этот ход
                turn = line.split(' ')
                y = int(turn[0]) 
                x = int(turn[1])
                player = int(turn[2])
                self.whos_turn = True if player == 1 else False
            
            else:
                turn = line.split(' ')
                y = int(turn[0]) 
                x = int(turn[1])
                player = int(turn[2])
                self.whos_turn = True if player == 1 else False

                game_logic.turn(y, x, player)
                if self.whos_turn:
                    history += f"Красные сделали ход в {y}:{x}\n"
                else:
                    history += f"Синие сделали ход в {y}:{x}\n"
   
        
        self.history_text.config(state = NORMAL)
        self.history_text.insert(INSERT, history)
        self.history_text.config(state = DISABLED)
        #рисуем только в конце
        self.place_stones(x * self.block_size + 20, y * self.block_size + 20)
        save_file.close()
    
    #новая игра
    def new_game(self):
        self.replay_mode = False
        self.pass_button.config(state = NORMAL)
        game_logic.update(game_logic.height, game_logic.width)
        self.history_text.config(state = NORMAL)
        self.history_text.delete('1.0', END) #удаляем историю
        self.history_text.config(state = DISABLED)
        self.draw_base_field(game_logic.width - 1, game_logic.height - 1)

    #сохранить игру
    def save(self):
        save_file = open('save.txt', 'w')
        save_file.write(f'{game_logic.height} {game_logic.width}\n')
        for i in game_logic.history:
            save_file.write(str(i) + "\n")
        save_file.close()

    #изменить размер игрового поля
    def change_size(self, x, y):
        if not self.replay_mode:
            game_logic.update(y + 1, x + 1)
            self.history_text.config(state = NORMAL)
            self.history_text.delete('1.0', END) #удаляем историю
            self.history_text.config(state = DISABLED)
            self.draw_base_field(x, y)

    #режим просмотра по шагам
    def replay(self):
        self.replay_mode = True
        self.turn_to_show = 1
        self.pass_button.config(state = DISABLED)
        self.history_text.config(state = NORMAL)
        self.history_text.delete('1.0', END) #удаляем историю
        self.history_text.config(state = DISABLED)
        try:
            save_file = open('save.txt', 'r')
        except:
            self.history_text.config(state = NORMAL)
            self.history_text.insert(INSERT, "Файл не найден\n")
            self.history_text.config(state = DISABLED)
            return
        
        self.list_for_replay = save_file.readlines()
        size = self.list_for_replay[0].split(' ')

        y = int(size[0])
        x = int(size[1])
        game_logic.update(y , x)
        self.draw_base_field(x - 1, y - 1)

    #показатель следующий ход в режиме просмотра по шагам
    def show_turn(self):
        turn = self.list_for_replay[self.turn_to_show].split(' ')
        self.turn_to_show += 1
        y = int(turn[0])
        x = int(turn[1])
        player = int(turn[2])
        self.whos_turn = True if player == 1 else False

        if self.turn_to_show == len(self.list_for_replay):
            self.replay_mode = False
            self.pass_button.config(state = NORMAL)
            self.place_stones(x * self.block_size + 20, y * self.block_size + 20)
            self.history_text.config(state = NORMAL)
            self.history_text.insert(INSERT, "Просмотр ходов закончен\n")
            self.history_text.config(state = DISABLED)
            return

        self.place_stones(x * self.block_size + 20, y * self.block_size + 20)
    
    #перерисовка игрового поля
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

        label = self.myfont.render(f'Черные: {game_logic.score_first}    Белые: {game_logic.score_second}', 1, (0,0,0))
        self.win.blit(label, (680, 30))

        if self.replay_mode:
            label = self.myfont.render('Для показа', 1, (0,0,0))
            self.win.blit(label, (710, 70))
            label = self.myfont.render('следующего хода', 1, (0,0,0))
            self.win.blit(label, (690, 90))
            label = self.myfont.render('нажимайте на SPACE', 1, (0,0,0))
            self.win.blit(label, (680, 110))

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

    #добавление информации о ходе в боковую панель
    def add_turn_info(self, x, y):
        self.history_text.config(state = NORMAL)
        if self.whos_turn:
            self.history_text.insert(INSERT, f"Красные сделали ход в {y}:{x}\n")
        else:
            self.history_text.insert(INSERT, f"Синие сделали ход в {y}:{x}\n")
        self.history_text.config(state = DISABLED)

    #добавить камень на поле
    def place_stones(self, x, y):
        field_size_x, field_size_y = self.game_surf.get_size()
        if x < 20 or y < 20 or x > field_size_x + 20 or y > field_size_y + 20: #выход за граница поля
            return
        else:
            tmp_x = round((x - 20) / self.block_size) #смотрим к какому пересечению мы ближе
            tmp_y = round((y - 20) / self.block_size)

            player = 1 if self.whos_turn else 2
            if game_logic.turn(tmp_y, tmp_x, player) and self.skipped_turns < 2:
                self.draw_base_field(game_logic.width - 1, game_logic.height - 1) #очистка поля
                self.add_turn_info(tmp_x, tmp_y)
                for i in range(game_logic.height): #рисуем поле заново
                    for j in range(game_logic.width):
                        tmp_x = 20 + self.block_size * j #вычисляем координаты
                        tmp_y = 20 + self.block_size * i

                        if game_logic.playing_field[i, j] == 1: #черный каменб
                            pygame.draw.circle(self.win, (255, 0, 0), (tmp_x, tmp_y), 17)
                        elif game_logic.playing_field[i, j] == 2: #белый камень
                            pygame.draw.circle(self.win, (0, 0, 255), (tmp_x, tmp_y), 17)
                self.whos_turn = not self.whos_turn
                self.skipped_turns = 0


            # tmp_x = 20 + self.block_size * tmp_x #вычисляем координаты этого пересечения
            # tmp_y = 20 + self.block_size * tmp_y

            
            pygame.display.update()

    #запуск
    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and not self.replay_mode:
                self.place_stones(event.pos[0], event.pos[1])
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.replay_mode:
                self.show_turn()
  
        pygame.display.update()  
        self.root.update_idletasks()
        self.root.update()


if __name__ == "__main__":   
    game_logic = GameGo(15, 15)      
    game = Game()
    run = True
    while run:
        game.run()

    pygame.quit()




