from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
       model = Post
       fields = ['title', 'category', 'text']
    
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
       
class PostComment(forms.ModelForm):
    class Meta:
       model = Comment
       fields = ['text']
       
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data