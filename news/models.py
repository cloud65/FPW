from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    @property
    def username(self):
        return self.user.username

    def update_rating(self):
        self.rating = 0
        for post in self.user_posts.all():
            self.rating += post.rating * 3
            for comment in post.comments.all():
                if comment.user != self:  # Исключим комментарии автора, т.к. они считается в цикле ниже
                    self.rating += comment.rating

        for comment in self.user.user_comments.all():
            self.rating += comment.rating
        self.save()

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers', related_name='subscribers')

    def __str__(self):
        return self.name


class Post(models.Model):
    NEWS = 1
    ARTICLE = 2
    choice_list = [(NEWS, "Новость"), (ARTICLE, "Статья")]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='user_posts')
    type_post = models.IntegerField(default=1, choices=choice_list)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, through='PostCategory', related_name='categories')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self, add=1):
        self.rating += add
        self.save()

    def dislike(self):
        self.like(-1)

    def preview(self):
        if len(self.text) <= 124:
            self.text
        return self.text[0:125] + "..."

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} / {self.category.name}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    date_create = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self, add=1):
        self.rating += add
        self.save()

    def dislike(self):
        self.like(-1)

    def __str__(self):
        return f"{self.user.username} / {self.post.title[0:30]}: {self.text[0:50]}"

    def get_absolute_url(self):
        return reverse('comment_detail', args=[str(self.id)])


class CategorySubscribers(models.Model):  # Служит для хранение подписок на категорию новостсей
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} / {self.category.name}"
