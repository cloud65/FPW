from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)
    rating = models.IntegerField(default=0)
    
    @property
    def username(self):
        return self.user.username
    
    def update_rating(self):
        self.rating = 0        
        for post in self.user_posts.all():
            self.rating += post.rating*3
            for comment in  post.comments.all():
                if comment.user!=self:  # Исключим комментарии автора, т.к. он считается в цикле ниже
                    self.rating += comment.rating            
        
        for comment in self.user.user_comments.all():
            self.rating += comment.rating
        self.save()
        


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    

class Post(models.Model):
    c_news = 1
    c_article = 2
    choice_list = [(c_news, "Новость"), (c_article, "Статья")]
        
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name='user_posts')
    type_post = models.IntegerField(default=1, choices=choice_list)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    
    
    def like(self, add=1):
        self.rating += add
        self.save()
    
    
    def dislike(self):
        self.like(-1)
        
    
    def preview(self):
        if len(self.text)<=124:
            self.text
        return self.text[0:125]+"..."
        

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user_comments')
    date_create = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    
    
    def like(self, add=1):
        self.rating += add
        self.save()
    
    
    def dislike(self):
        self.like(-1)