from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post, Author
from .forms import PostForm
from .filters import PostFilter


class NewsList(ListView):
    model = Post
    
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_create'

    template_name = 'posts.html'
    context_object_name = 'posts'
    
    paginate_by = 10
    
    
     # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['search']  = 'search' in self.request.path
        return context


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному объекту
    model = Post
    template_name = 'post-detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_editable'] = context['post'].author==Author.objects.get(user=self.request.user)
        context['is_news'] = context['post'].type_post==1
        return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post-edit.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)
    


class NewsCreate(PostCreate):   
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = Post.NEWS
        return super().form_valid(form)


class ArticlesCreate(PostCreate):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = Post.ARTICLE
        return super().form_valid(form)

    
class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post-edit.html'
    
    
class PostDelete(DeleteView):
    model = Post
    template_name = 'post-delete.html'
    success_url = reverse_lazy('post_list')
    
   