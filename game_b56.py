import os


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



def render_cell(val):
    sym={0: " ", -1: get_color('red')+"o"+get_color('yellow'), 1: get_color('green')+"x"+get_color('yellow')}
    return sym[val]
 

def render(M):
    size = len(M[0])
    
    left_interval = " "*20
    
    cls()
    title = ' | '.join([str(i) for i in range(1, size+1)])
    
    print(f"{get_color('yellow')}{left_interval} | {title} |")
    
    for i, R in enumerate(M):
        print(f"{left_interval} -{'----'*size}")
        row = " | ".join(map(render_cell, R))            
        print(f"{left_interval}{i+1}| {row} |")
         
    print(f"{left_interval} -{'----'*size}")
    

def check(M):  
    list_res = [set(), set()] # Для проверки Победителя или ничьей
    size = len(M)
    for i in range(size):   #Диагонали
        list_res[0].add(M[i][i])
        list_res[1].add(M[i][size-1-i])

    for row in M:   #Сбор по строкам
        list_res.append(set(row))
        
    for col in zip(*M):   #Сбор по столбцам
        list_res.append(set(col))
    
    for n in list_res: #Ищем победителя
        if {1}==n or {-1}==n:
            return list(n)[0]
    
    is_none = True
    for n in list_res: # Ищем ничью
        is_none = is_none and {1, -1}<=n
    if is_none:
        return None
    
    return 0


def input_name(text, color):
    text = "\033[00m"+text+color
    result = input(text)
    while not result:
       print('\033[A\033[A')
       result = input(text)    
    return result
    
  
def input_cell(name, color, M):
    text = f"{color}{name}{get_color()}, введите адрес ячейки [Строка Столбец]: {color}"    
    print("\n")
    while True:       
        print('\033[A' + " "*70 + '\033[A')
        str_result = "".join(c for c in input(text) if  c.isdecimal())
        str_result = str_result[0:2]
        
        result = (int(str_result)//10, int(str_result)%10)
              
        if 1<=result[0]<=3 and 1<=result[1]<=3 and M[result[0]-1][result[1]-1]==0:
            break
      
    return result
    
    
def show_result(chk, name1, name2, color1, color2):
    if chk is None:
        print("Ничья. Победила дружба.")
    elif chk==1:
        print(get_color("cyan")+"Победитель: "+color1+name1)
    else:
        print(get_color("cyan")+"Победитель: "+color2+name2)
    

def main(size=3):
    M = [[0 for i in range(1, size+1)] for j in range(1, size+1)]
    
    color1 = get_color("green")
    color2 = get_color("red")
    
    cls()
    print('Введите имена игроков:')
    name1 = input_name("Первый игрок (играет [x]): ", color1)
    name2 = input_name("Второй игрок (играет [o]): ", color2)
        
    render(M)
    while True:
        i, j = input_cell(name1, color1, M)
        M[i-1][j-1] = 1
        render(M)
        
        result = check(M)
        if result!=0:
            show_result(result, name1, name2, color1, color2)
            break
        
        i, j = input_cell(name2, color2, M)
        M[i-1][j-1] = -1        
        render(M)
        
        result = check(M)
        if result!=0:
            show_result(result, name1, name2, color1, color2)
            break
           
    print(get_color())


if __name__ == "__main__":
    main()
    
