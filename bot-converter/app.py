from os.path import join as join_path
from  configparser import ConfigParser
from telebot import TeleBot
from telebot.types import Message as tbMessage
from extensions import * 

class App:  
    def __init__(self, path='.'):   # path - каталог файла config.ini       
        config = ConfigParser()
        config.sections()
        config.read(join_path(path, 'config.ini'), encoding='utf-8')
        token = config.get('main', 'token') # Получаем токен
        
        self.keys = dict()
        for item in config['values']:   # читаем доступную валюту из секции values
            self.keys[config.get('values', item).lower()] = item.upper()
        
        self.__bot = TeleBot(token)   # Созаем бота и назначаем обработчики сообщений
        self.__bot.register_message_handler(self.send_help, commands=['start', 'help', '?'])
        self.__bot.register_message_handler(self.send_values, commands=['values'])
        self.__bot.register_message_handler(self.send_convert, content_types=['text'])
    
    
    def send_help(self, message: tbMessage):   # ответ на help, start и ?
        msg = """<b>Бот для конвертации валют</b>
Для расчеты отправьте сообщение боту в следующем формате:
<code>{название валюты} {название новой валюты} {сумма исходной валюты}</code>
Например:
<b>доллар рубль 1000</b>
            
Для получение списка доступных валют используйте команду: /values"""
        self.__bot.send_message(message.chat.id, msg, parse_mode="HTML")
        
        
    def send_values(self, message: tbMessage):   # ответ на values
        msg = "\n".join([ f"<b>{i[0]}</b> <u>({i[1]})</u>" for i in self.keys.items() ])
        self.__bot.send_message(message.chat.id, f"Доступные валюты:\n{msg}", parse_mode="HTML")
        
    
    def send_error(self, message: tbMessage, error: str):
        self.__bot.reply_to(message, error, parse_mode="HTML")
    
    
    def check_user_message(self, msg: str):
        list_msg = [i.lower() for i in msg.split(' ') if i and not i.isspace()]  # разобъем строку и удалим лишние пробелы
        if len(list_msg)!=3:
            raise APIException('Неверное количество параметров.')
        
        for i in range(2):
            if not self.keys.get(list_msg[i]):
                raise APIException(f'Неверное наименование валюты: {list_msg[i]}')
                
        if(list_msg[0]==list_msg[1]):
            raise APIException(f'Валюты не должны совпадать')
        
        try:
            amount = float(list_msg[2])
        except ValueError as e:
            print(list_msg)
            raise APIException('Третий параметр должен быть числом.')
            
        return (
            (self.keys.get(list_msg[0]), list_msg[0]),
            (self.keys.get(list_msg[1]), list_msg[1]),
            amount
            )   
        
            
    
    def send_convert(self, message: tbMessage):  # непосредственно конвертация                
        try:
            base, quote, amount = self.check_user_message(message.text) # Парсим и проверяем введеные данные
            result = APIConverter.get_price(base[0], quote[0], amount)
        except APIException as e:
            self.send_error(message, f"Ошибка ввода данных:\n<b>{e}</b>")
            return
        except ExtAPIException as e:
            self.send_error(message, f"Ошибка обращения к сервису:\n<b>{e}</b>")
            return
        
        msg = f"Стоимость <u>{amount:.2f}</u> <u>{base[0]}</u> ({base[1]}) равно <b>{result:.2f}</b> <u>{quote[0]}</u> ({quote[1]})"
        self.__bot.reply_to(message, msg, parse_mode="HTML")
     
     
    def run(self):  # основная петля программы
        name = self.__bot.get_me().first_name
        print(f'Telebot {name} is started...')
        self.__bot.polling(none_stop=True)
        
        
        
if __name__ == "__main__":
    app = App(r'Z:\work\python\edu2\5.2')
    app.run()