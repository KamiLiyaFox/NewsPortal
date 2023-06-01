from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsSearch, NewsDelete, CategoryListView, subscribe, unsubscribe


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем новостям у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(), name='news_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('search/', NewsSearch.as_view(), name='news_search'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
   # path('index/', IndexView.as_view()),
]