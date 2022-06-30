from django import forms
from django_filters import FilterSet, CharFilter, DateFilter, AllValuesMultipleFilter
from .models import Post

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains', label='Заголовок')       
    #date_start = django_filters.DateFilter(field_name="date_create", lookup_type='gte')
    
    date_start = DateFilter(field_name='date_create',
                               widget= forms.DateInput(attrs={'type': 'date'}),
                               lookup_expr='gt', label='Публикация позже'
                           )
                           
    class Meta:
        model = Post
        fields = [  'title',  'date_start', 'category' ]
        labels = { 'category': 'Категории' }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['category'].label = 'Категория'