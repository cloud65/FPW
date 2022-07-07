from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .filters import PostFilter
from .forms import PostForm, UserForm
from .models import Post, Author


def userpage(request):
    user_form = UserForm(instance=request.user)
    is_author = request.user.groups.filter(name='authors').exists()
    return render(request=request, template_name="user.html",
                  context={"user": request.user, "user_form": user_form, 'is_author': is_author})


@login_required
def set_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=request.user)
    return redirect('/profile/')


class NewsList(ListView):
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_create'

    template_name = 'post/posts.html'
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
        context['search'] = 'search' in self.request.path
        return context


class NewsDetail(PermissionRequiredMixin, DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному объекту
    model = Post
    permission_required = ('news.view_post',)

    template_name = 'post/post-detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_news'] = context['post'].type_post == 1
        context['is_editable'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post/post-edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        try:
            post.author = Author.objects.get(user=self.request.user)
        except Author.DoesNotExist as e:
            raise e
            # post.author = Author.objects.create(user=self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Post
    permission_required = ('news.change_post',)
    form_class = PostForm
    template_name = 'post/post-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    permission_required = ('news.delete_post',)
    template_name = 'post/post-delete.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
