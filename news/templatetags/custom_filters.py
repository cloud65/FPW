from django import template
from news import censor_words  

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    words = censor_words.get_words()
    text_words=value.split(' ')
    for i, word in enumerate(text_words):
        if word.lower() in words:
            text_words[i] = word[0]+'*'*(len(word)-1)      
    return ' '.join(text_words)
    
