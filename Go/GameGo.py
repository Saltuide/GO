import numpy as np 
from queue import Queue

class Turn:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player

class GameGo:
    def __init__(self, height, width):
        #храним высоту и ширину поля
        self.height = height
        self.width = width
        #создаем игровое поле
        self.playing_field = np.zeros((height, width), np.uint8)
        #объявляем переменные для хранения счета
        self.score_first = 0
        self.score_second = 0
        #история
        self.history = []

    #проверка на КО
    def check_KO(self, x, y):
        if (len(self.history) > 2):
            return (self.history[len(self.history) - 2].x == x and self.history[len(self.history) - 2].y == y)
        else:
            return False

    #проверяет, какие группы умирают
    def check_eat(self, player):
        used = [[False for i in range(self.width)] for j in range(self.height)]
        dead = []
        for i in range(self.height):
            for j in range(self.width):
                ##нашли новую группу
                if (self.playing_field[i][j] == player and not used[i][j]):
                    q = Queue()
                    q.put((i, j))
                    used[i][j] = True
                    dame = 0
                    group = []
                    while (not q.empty()):
                        (x, y) = q.get()
                        group.append((x, y))
                        if (x > 0 and not used[x - 1][y]):
                            if (self.playing_field[x - 1][y] == player):
                                q.put((x - 1, y))
                                used[x - 1][y] = True
                            if (self.playing_field[x - 1][y] == 0):
                                dame += 1
                        if (x < self.height - 1 and not used[x + 1][y]):
                            if (self.playing_field[x + 1][y] == player):
                                q.put((x + 1, y))
                                used[x + 1][y] = True
                            if (self.playing_field[x + 1][y] == 0):
                                dame += 1
                        if (y > 0 and not used[x][y - 1]):
                            if (self.playing_field[x][y - 1] == player):
                                q.put((x, y - 1))
                                used[x][y - 1] = True
                            if (self.playing_field[x][y - 1] == 0):
                                dame += 1
                        if (y < self.width - 1 and not used[x][y + 1]):
                            if (self.playing_field[x][y + 1] == player):
                                q.put((x, y + 1))
                                used[x][y + 1] = True
                            if (self.playing_field[x][y + 1] == 0):
                                dame += 1
                    if (dame == 0):
                        for (q1, q2) in group:
                            dead.append((q1, q2))

        if (len(dead) == 0):
            ##никакие группы игрока player не умирают
            return (False, [])
        else:
            ##в результате хода какие-то группы игрока player были убиты
            # print(dead)
            return (True, dead)

    #заявочка на ход
    def turn(self, x, y, player):
        # если занято, сразу нахер
        if (self.playing_field[x][y] != 0):
            return False
        #враг
        enemy = 1 if player == 2 else 2
        #"дамэ" - дыхательные пункты
        dame = 0
        if (x > 0 and self.playing_field[x - 1][y] != enemy):
            dame += 1
        if (x < self.height - 1 and self.playing_field[x + 1][y] != enemy):
            dame += 1
        if (y > 0 and self.playing_field[x][y - 1] != enemy):
            dame += 1
        if (y < self.width - 1 and self.playing_field[x][y + 1] != enemy):
            dame += 1

        #че будет, если я схожу
        self.playing_field[x][y] = player
        (check1, dead1) = self.check_eat(enemy)
        (check2, dead2) = self.check_eat(player)
        
        print("player: ", dead1)
        print("enemy: ", dead2)
        print("self player", player)
        print("self enemy", enemy)
        print(self.playing_field)
        
        #если игрок делает ход, который может убить его группу
        if check2:
            print("111 строка !!!!")
            if (not self.check_KO(x, y) and check1):
                print("!!!")
                if player == 1:
                    self.score_first += len(dead2)
                else:
                    self.score_second += len(dead1)
                #бежим по всем убитым клеточкам противника и освобождаем
                for q in range(len(dead1)):
                    (i, j) = dead1[q]
                    self.playing_field[i][j] = 0
            else:
                self.playing_field[x][y] = 0
                print('произошел суицид')
                return False
            return True
        else:
            #увеличиваем счетчик очков
            if player == 1:
                self.score_first += len(dead2)
            else:
                self.score_second += len(dead1)
            #бежим по всем убитым клеточкам и освобождаем
            for q in range(len(dead1)):
                (i, j) = dead1[q]
                self.playing_field[i][j] = 0
            # print(self.playing_field)
        return True
        

    def bfs(self, player):
        used = [[False for i in range(self.width)] for j in range(self.height)]
        q = Queue()
        for i in range(self.height):
            for j in range(self.width):
                if (self.playing_field[i][j] == player):
                    used[i][j] = True
                    q.put((i, j))
        
        while (not q.empty()):
            (x, y) = q.get()
            if (x > 0 and self.playing_field[x - 1][y] == 0 and not used[x - 1][y]):
                used[x - 1][y] = True
                q.put((x - 1, y))
            if (x < self.height - 1 and self.playing_field[x + 1][y] == 0 and not used[x + 1][y]):
                used[x + 1][y] = True
                q.put((x + 1, y))
            if (y > 0 and self.playing_field[x][y - 1] == 0 and not used[x][y - 1]):
                used[x][y - 1] = True
                q.put((x, y - 1))
            if (y < self.width - 1 and self.playing_field[x][y + 1] == 0 and not used[x][y + 1]):
                used[x][y + 1] = True
                q.put((x, y + 1))
            
        ans = 0
        for i in range(self.height):
            for j in range(self.width):
                if (self.playing_field[i][j] == 0 and used[i][j] == False):
                    ans += 1
        return ans


    def result(self):
        return (f'результат первого игрока = {self.bfs(2)}\nрезультат второго игрока = {self.bfs(1)}')
        # print(used)



# kq = GameGo(5, 5)
# kq.playing_field = [
#     [0, 1, 0, 2, 0],
#     [0, 1, 0, 2, 0],
#     [0, 1, 0, 2, 0],
#     [0, 1, 0, 2, 2],
#     [0, 1, 0, 0, 0]
# ]

# print(kq.turn(0, 0, 1))
# print(kq.turn(2, 3, 2))
# print(kq.turn(0, 1, 1))
# print(kq.turn(3, 2, 2))
# print(kq.turn(0, 2, 1))
# print(kq.turn(3, 4, 2))
# print(kq.turn(0, 3, 1))
# print(kq.turn(4, 3, 2))
# print(kq.turn(3, 3, 1))

# print(kp.playing_field)
# print(kq.playing_field)




# print('\n')

# print(kq.playing_field)


#############################################################################
#пример с вики

go = GameGo(9, 9)

go.playing_field = [
    [0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 2, 1, 1, 1],
    [0, 0, 0, 0, 1, 2, 2, 2, 2],
    [0, 1, 1, 1, 2, 0, 0, 0, 0],
    [1, 1, 2, 2, 2, 2, 0, 0, 0],
    [1, 2, 0, 2, 0, 2, 0, 0, 0],
    [1, 2, 0, 0, 2, 0, 0, 0, 0],
    [2, 2, 2, 0, 2, 0, 0, 0, 0]
]

# go.playing_field = [
#     [2, 2, 1, 0, 0, 0, 1, 0, 0],
#     [2, 0, 1, 0, 1, 1, 0, 1, 0],
#     [1, 1, 1, 0, 1, 2, 1, 1, 1],
#     [0, 0, 0, 0, 1, 2, 2, 2, 2],
#     [0, 1, 1, 1, 2, 0, 0, 0, 0],
#     [1, 1, 2, 2, 2, 2, 0, 0, 0],
#     [1, 2, 0, 2, 0, 2, 0, 0, 0],
#     [1, 2, 0, 0, 2, 0, 0, 0, 0],
#     [2, 2, 2, 0, 2, 0, 0, 0, 0]
# ]

# go = GameGo(5, 5)
# go.playing_field = [
#     [0, 0, 0, 0, 0],
#     [0, 1, 2, 0, 0],
#     [1, 0, 1, 2, 0],
#     [0, 1, 2, 0, 0],
#     [0, 0, 0, 0, 0]
# ]
# print(go.turn(2, 1, 2))
# for i in go.playing_field:
#     print(i)

print(go.result()) #20 23
# print(go.check_eat(1))
# print(go.turn(1, 1, 2))

