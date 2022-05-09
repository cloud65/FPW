import os
from random import randint


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def get_color(name=None):
    color={
        None: "\033[00m", 
        "red": "\033[01;31m", 
        "green": "\033[01;32m", 
        "yellow": "\033[01;33m", 
        "blue": "\033[01;34m", 
        "cyan": "\033[01;36m"
    }
    return color[name]


def set_cursor(x, y):
    print(f'\033[{y};{x}H', end="")


#=================================================================
class Dot:
    def __init__(self, x, y):
        self.x, self.y = x, y


    def __eq__(self, dot):
        return self.x==dot.x and self.y==dot.y
        
        
    def __str__(self):
        return f"({self.x}, {self.y})"


#=================================================================
class Ship:
    @staticmethod
    def vertical(): # Константы положения кораблей, используются числа для рандома
        return 0


    @staticmethod
    def horizontal():
        return 1


    def __init__(self, dot, size, course):
        self.__dots = list()
        self.size = size
        for i in range(size): #сразу создаем все точки корабля
            x = i+dot.x if course==Ship.vertical() else dot.x
            y = i+dot.y if course==Ship.horizontal() else dot.y
            self.__dots.append(Dot(x, y))

        self.dots_killed = list()        
        self.__area = list()
        for dot in self.__dots: #создаем точки контура.
            for x in range(dot.x-1, dot.x+2):  
                for y in range(dot.y-1, dot.y+2):
                    area_dot = Dot(x, y);
                    if not area_dot in self.__area:
                        self.__area.append(area_dot)


    def __str__(self):
        return ", ".join([f"({i.x}, {i.y})" for i in self.__dots])


    def dots(self):  # Точки корабля
        return self.__dots
        
        
    def area(self): # Вся "площадь" корабля для проверки пересечиний
        return self.__area
        
   
    def contour(self): #Контур корабля
        result = list()
        for dot in self.area():
            if not dot in self.dots():
                result.append(dot)
        return result
        
        
    def crossing(self, other): # Для проверки пересечений кораблей и контура
        result = False       
        for dot in self.dots():
            result = result or dot in other.area()
        return result
        
        
    def add_kill_dot(self, dot): # Добаляем точку, если она попала в корабль
        if dot in self.__dots:
            self.dots_killed.append(dot)


    @property
    def is_killed(self):
        return len(self.dots_killed)==self.size


#=================================================================
class Board:
    def types_ship(self): # Типы кораблей игры
        types = list()
        for i in range(1,3):
            types.append((i, 4-i))
        types.append((4, 1))  # Без понятия почему должно быть четыре, а не три, но так сказано в задании    
        return types
        
    
    def random(self):
        list_types = self.types_ship()
        max_ships = 1
        count_ships = 0        
        while count_ships<max_ships: # Выполняем, пока не размещены все корабли. 
            self.clear()
            max_ships=0
            count_ships = 0
            for count, size in list_types:
                max_ships +=count
                for c in range(count):
                    for _ in range(1000):  # Бывают комбинации, когда нельзя расположить все корабли. 
                        first_dot = Dot(randint(1, self.size), randint(1, self.size)) 
                        ship = Ship(first_dot, size, randint(0, 1))
                        try: 
                            self.add_ship(ship)
                        except ValueError as e:
                            continue # Если не удалось расположить корабль, повторяем попытку
                        count_ships += 1
                        break    
                        
    
    def __init__(self, name, hid=False, left=0, size=6, random=True):
        self.hid = hid
        self.left = left
        self.ships = list()
        self.stats = list() # "Стрелянные точки"
        self.size = size # Размер поля
        self.name = name
        self.score = 0 # Количество попаданий
        self.steps = 0 # Количество выстрелов
        self.error = None
        if random:
           self.random() # Выполним рандамное заполнение
           
           
    def set_name(self, name):
        self.name = name
    
    
    def clear(self):
        self.ships = list()
        self.stats = list()
        self.score = 0

    
    def get_name(self):
        return self.name
        

    def set_error(self, text=None):
        self.error = text
        
        
    def is_end(self):
        result = True
        for ship in self.ships:
            result = result and ship.is_killed
        return result


    def add_ship(self, ship):
        first_dot = ship.dots()[0]
        last_dot = ship.dots()[-1]
        if self.out(first_dot) or self.out(last_dot):
            raise ValueError("Неверные координаты или размеры")        
        for s in self.ships:
            if ship.crossing(s):
                raise ValueError("Есть пересечения с другими кораблями")            
        self.ships.append(ship)


    def out(self, dot):
        return not (0<dot.x<=self.size and 0<dot.y<=self.size)
    
    
    def print(self, row, text):
        set_cursor(self.left, row)
        print(text, end="")
        

    def print_dot(self, dot, ch = chr(9608), color=None): # Вывод точек
        if self.out(dot): #Не выводим точки вне поля
            return
        set_cursor(self.left+4+(dot.y-1)*4, 4+(dot.x-1)*2)
        print(get_color(color), ch*4, end="", sep="")
        set_cursor(self.left+4+(dot.y-1)*4, 5+(dot.x-1)*2)
        print(get_color(color), ch*4, end="", sep="")

    
    def bottom(self): #Кординаты нижней части экрана под досками
        return self.size*2+10


    def render(self): # Чертим доску с кораблями и выстрелами
        yellow = get_color("yellow")
        green = get_color("green")
        red = get_color("red")
        normal = get_color()
        sea = chr(9617)
        self.print(1, f"{normal}Игрок: {green}{self.name}{normal}")
        self.print(2, "   " + "".join(f"| {i+1} " for i in range(self.size)) + " |")
        self.print(3, f"---|{'-'*(self.size*4)}|---")
        for i in range(self.size):
            self.print(4+i*2, f" {i+1} |{sea*(self.size*4)}| {i+1}")
            self.print(4+i*2+1, f"---|{sea*(self.size*4)}|---")
        self.print(self.size*2+4, f"   |{'-'*(self.size*4)}|")
        self.print(self.size*2+5, "   " + "".join(f"| {i+1} " for i in range(self.size)) + " |")
        self.print(self.size*2+6, f"""  Выстрелов: {yellow}{self.steps}{normal}   Попаданий: {green}{self.score}{normal}""")
            
        text_error = " "*(self.size*4+20) # Выводим ошибку или очищаем предыдущую ошибку
        if self.error:
            self.print(self.size*2+7, text_error)  
            text_error = f"  Ошибка: {red}{self.error}{normal}"            
        self.print(self.size*2+7, text_error)        
        
        for dot in self.stats: # Выводим стреляные точки
            self.print_dot(dot, ch=chr(9619), color="blue")
        
        for ship in self.ships:
            for dot in ship.dots():
                if not self.hid: #Выводим свой корабль
                    self.print_dot(dot, color="green")                    
                if dot in ship.dots_killed: #Выводим подбитые точки                
                    self.print_dot(dot, color="red")
            if ship.is_killed: # Если корабль убит, то обводим его по контуру
                for dot in ship.contour():
                    self.stats.append(dot)
                    self.print_dot(dot, ch=chr(9619), color="blue")


    def shot(self, dot): # Произведем выстрел
        result = False
        if self.out(dot):
            raise ValueError("Точка за пределеми поля")
        if dot in self.stats:
            raise ValueError("Эта точка уже открыта")
        self.stats.append(dot)
        self.steps += 1
        for ship in self.ships:
            ship.add_kill_dot(dot)
            if dot in ship.dots_killed:
                self.score += 1  # Добавляем очки
                result = True
            if ship.is_killed: # Если корабль убит, добавляем контур в "использованные" точки
                for с_dot in ship.contour(): 
                    self.stats.append(dot)
        return result
                
   
#=================================================================
class Player:
    def __init__(self, board, rival_board):
        self.board = board
        self.rival_board = rival_board
        
        
    def ask(self):
        pass
        
    
    def move(self, show_error=True): # Выполнение хода. Для компьютера ошибок не показываем
        while True:
            if self.rival_board.is_end():
                break
            try:
                self.board.set_error()
                set_cursor(1, self.board.bottom())
                dot = self.ask()
                result = self.rival_board.shot(dot)
                self.rival_board.render()
                if not result:
                    break                
            except ValueError as e:
                if show_error:
                    self.rival_board.set_error(str(e))
                    self.rival_board.render()   
            
    
#=================================================================
class User(Player):
    def ask(self):        
        name = self.board.get_name()
        color = get_color("green")
        text = f"{color}{name}{get_color()}, введите точку выстрела [Строка Столбец]: {color}"
        print(text)
        print(f'\033[A{" "*70}\033[A') # чтобы лишний раз не рендерить, просто очистим строку выше
        str_result = "".join(c for c in input(text) if  c.isdecimal()) # получаем input и оставляем цифры
        str_result = str_result[0:2]
        if not str_result:
            raise ValueError("Вы ввели неверные координаты")
        return Dot(int(str_result)//10, int(str_result)%10)
            
            
#=================================================================
class Ai(Player):
    def ask(self):
        return Dot(randint(1, self.board.size), randint(1, self.board.size))


#=================================================================
class Game:             
    def __init__(self):
        self.user_board = Board("Игрок", hid=False, left=10) 
        self.ai_board = Board("Компьютер", hid=True, left=60) 
        self.user = User(self.user_board, self.ai_board)        
        self.ai = Ai(self.ai_board, self.user_board)
    
    
    def greet(self):
        yellow = get_color("yellow")
        green = get_color("green")
        blue = get_color("blue")
        red = get_color("red")
        normal = get_color()
        msg = f"""
        {yellow}Добро пожадовать в игру {green}"Морской бой"{normal}
        Цель игры: {yellow}Разбить флот противника, потопив все его корабли.{normal}
        
        Будут выведены два поля 6x6: левое - Ваше, правое - Компьютера.
        Корабли будут расстановленны случайным образом.
        {yellow}Для "выстрела" следует вводить координаты ячейки поля противника.
        Координаты вводятся ввиде двух цифр, цифры могут быть разденны знаком.
        Если Вы введете более двух цифр, будут {red}приняты первые две{normal}
        Примеры: {green} 66   {normal}-точка (6, 6)
                 {green} 2 2  {normal}-точка (2, 2)
                 {green} 3-1  {normal}-точка (3, 1)
                 {green} 321  {normal}-точка (3, 2)
        {yellow}Для продолжения введите свое имя ({normal}Enter - выход{yellow}):{normal}"""        
        user_name = input(msg)
        if not user_name:
            exit()
        self.user_board.set_name(user_name)
    
    
    def render(self):
        self.user_board.render() 
        self.ai_board.render()
    
    
    def show_champion(self, user):
        set_cursor(1, user.board.bottom())
        print(f'{get_color("yellow")} Победитель: {get_color("green")}{user.board.get_name()}{get_color()}{" "*50}')
    
        
    def loop(self):
        cls()
        self.render()
        while True:            
            self.user.move()
            self.render()
            if self.ai_board.is_end():
                self.show_champion(self.user)
                break
                
            self.ai.move(False)
            self.render()
            if self.user_board.is_end():
                self.show_champion(self.ai)
                break
   
    
    def start(self):
        cls()
        self.greet()
        self.loop()
        
        
#============================================================
if __name__=="__main__":
    game = Game()
    game.start()
    #test()
