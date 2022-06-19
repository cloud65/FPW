from django.db import models

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User)
    current_rating = models.IntegerField()
    


class Category(models.Model):
    name = models.CharField(max=150, unique=True)
    

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    type_post = models.IntegerField(default=1, choices=Post.choice_list())
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max=512)
    text = models.TextField()
    rating = models.IntegerField()

    
    @staticmethod
    def choice_list(self):
        return {
            1: "Новость",
            2: "Статья"
        }
        

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField()
    