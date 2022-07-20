from django.urls import path
# Импортируем созданное нами представление
from .views import * 


urlpatterns = [
   path('', NewsList.as_view(), name='post_list'), 
   path('news/', NewsList.as_view(), name='post_list'),   
   path('view/<int:pk>', NewsDetail.as_view(), name='post_detail'),
   
   path('news/search', NewsList.as_view(), name='post_list'),
   
   path('news/create', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit', PostUpdate.as_view(), name='news_edit'),
   path('news/<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   
   path('articles/create', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit', PostUpdate.as_view(), name='articles_edit'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),

   path('news/set-subscribe/<int:category>', set_subscribe, name='set_subscribe')
]