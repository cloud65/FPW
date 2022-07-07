from requests import get 
from json import loads

class APIException(Exception):
    pass
    
    
class ExtAPIException(Exception):
    pass   
  
  
class APIConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount:int):
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote}&from={base}&amount={amount}"  
        headers= {"apikey": "L3u7LHk0WzzNgtpjvdUu895Mgvi3hXiu"}
        response = get(url, headers=headers)

        if response.status_code!=200:
            raise ExtAPIException(response.text)
        
        result = loads(response.text)
        if result.get("success"):
            return result.get("result")
        
        msg = result.get("message")
        if msg:
            raise ExtAPIException(msg)
        else:
            raise ExtAPIException("Неизвестная ошибка")
        
        
        
if __name__ == "__main__":
    print(APIConverter.get_price('USD', 'EUR', 1))