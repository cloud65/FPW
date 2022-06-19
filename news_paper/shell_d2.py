#!python3 manage.py shell
from news.models import *

# 1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).
user1 = User.objects.create_user('user3')
user2 = User.objects.create_user('user4')
user3 = User.objects.create_user('user5')
user4 = User.objects.create_user('user6')
user5 = User.objects.create_user('user9')
user6 = User.objects.create_user('user8')

# 2. Создать два объекта модели Author, связанные с пользователями.
author1 = Author.objects.create(user=User.objects.create_user('user1'))
author2 = Author.objects.create(user=User.objects.create_user('user2'))


# 3. Добавить 4 категории в модель Category.
cat1 = Category.objects.create(name='Проишествия')
cat2 = Category.objects.create(name='Политика')
cat3 = Category.objects.create(name='Бизнес')
cat4 = Category.objects.create(name='Финансы')
cat5 = Category.objects.create(name='МЧС')
cat6 = Category.objects.create(name='Путешествия')
cat7 = Category.objects.create(name='Природа')


# 4 Добавить 2 статьи и 1 новость.
# Новость
post1 = Post.objects.create(
    author = author1, 
    type_post = Post.c_news, 
    title = 'У озера Тауро на Сахалине потушили природный пожар', 
    text = """18 июня в 16:16 диспетчеру углегорского пожарно-спасательного гарнизона поступило сообщение о возгорании сухой растительности в районе озера Тауро. 
    Пожарный расчет прибыл через 19 минут. К этому моменту растительность горела на площади 1 Га.
    Возгорание было локализовано в 17:45, а в 18:06 — полностью ликвидировано. В тушении участвовали 4 человека и 1 единица техники 
    противопожарной службы Сахалинской области. Погибших и пострадавших нет. Причины возгорания устанавливаются, 
    сообщает ИА Сах.ком со ссылкой на пресс-службу ГУ МЧС России по Сахалинской области."""
    )

# Статья 1
post2 = Post.objects.create(
    author = author1, 
    type_post = Post.c_article, 
    title = 'Старые крепости', 
    text = """Чжурчжэни оставили заметный след в истории древнего Дальнего Востока. Историки склонны отнести к чжурчжэньской цивилизации (IX-XIII вв.) остатки крепостных сооружений на полуострове Крильон, а также известные из документальных источников, но исчезнувшие ныне крепости-городища в районе Усть-Пугачево, Александровке-Сахалинском. История этого народа меня захватила и, узнав, что в Долинском районе находятся остатки сооружений, похожих на средневековые крепости, я оправился к реке Найбе."""
    ) 

# Статья 2
post3 = Post.objects.create(
    author = author2, 
    type_post = Post.c_article, 
    title = 'Амурский щит', 
    text = """После моего прошлогоднего путешествия на яхте "Отрада" вокруг Сахалина по следам Амурской экспедиции капитана Невельского осталось много путевых записок...
История тихоокеанского побережья России крайне интересна, но мало кому, к сожалению, знакома...
28 июля 2013 года. Ветер встречный. Яхту встряхивает, как автомобиль на плохой грунтовой дороге. Вновь надо встраиваться в ритм движущейся воды, где тебе верные слуги — мачты паруса, двигатель, навигационное оборудование…"""
    )


# 5 Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).    
post1.category.add(cat1)
post1.category.add(cat5)

post2.category.add(cat6)
post2.category.add(cat7)

post3.category.add(cat6)
post3.category.add(cat7)


# 6 Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
comments = list()
comments.append(Comment.objects.create(post = post1, user = user2, text = "Молодцы пожарные. Быстро среагировали"))
comments.append(Comment.objects.create(post = post2, user = user5, text = "Спасибо. Очень итересная статья"))
comments.append(Comment.objects.create(post = post2, user = user4, text = "Очень итересно. Хочу посетить"))
comments.append(Comment.objects.create(post = post3, user = user6, text = "Спасибо. Очень итересная статья"))
comments.append(Comment.objects.create(post = post3, user = user3, text = "Очень итересная статья"))

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
# "Накрутим" все случайным образом, но лайков больше
from random import randint
for obj in [post1, post2, post3] + comments:
    for _ in range(randint(10, 100)):
        if randint(0, 8)>2:
            obj.like()
        else:
            obj.dislike()


# 8. Обновить рейтинги пользователей.
for a in Author.objects.all():
    a.update_rating()


# 9 Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
author_top = Author.objects.all().order_by('-rating')[0]
print(f"Рейтинг {author_top.username}: {author_top.rating}")


# 10 Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
post = Post.objects.all().order_by('-rating')[0]
print(f"Дата: {post.date_create.strftime('%d.%m.%y')},  автор: {post.author.username}, рейтинг: {post.rating}  ")
print(f" Название: {post.title}")
print(f"{post.preview()}  ")


# 11 Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
for c in post.comments.all():
    print(f"{c.user.username} (добавлен: {c.date_create}, рейтинг: {c.rating}): {c.text}")