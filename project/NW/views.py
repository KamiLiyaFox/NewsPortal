from datetime import datetime
from django.shortcuts import render
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from django.core.paginator import Paginator
from.filters import *
from django.urls import reverse_lazy
from .forms import *
from django.http import HttpResponseRedirect


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = News
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_pub'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    # # Переопределяем функцию получения списка товаров
    # def get_queryset(self):
    #     # Получаем обычный запрос
    #     queryset = super().get_queryset()
    #     # Используем наш класс фильтрации.
    #     # self.request.GET содержит объект QueryDict, который мы рассматривали
    #     # в этом юните ранее.
    #     # Сохраняем нашу фильтрацию в объекте класса,
    #     # чтобы потом добавить в контекст и использовать в шаблоне.
    #     self.filterset = NewsFilter(self.request.GET, queryset)
    #     # Возвращаем из функции отфильтрованный список товаров
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Добавляем в контекст объект фильтрации.
    #     context['filterset'] = self.filterset
    #     return context

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }

    # def get_context_data(self, **kwargs):
    #     # С помощью super() мы обращаемся к родительским классам
    #     # и вызываем у них метод get_context_data с теми же аргументами,
    #     # что и были переданы нам.
    #     # В ответе мы должны получить словарь.
    #     context = super().get_context_data(**kwargs)
    #     # К словарю добавим текущую дату в ключ 'time_now'.
    #     context['time_now'] = datetime.utcnow()
    #     # Добавим ещё одну пустую переменную,
    #     # чтобы на её примере рассмотреть работу ещё одного фильтра.
    #     context['news_article'] = None
    #     return context


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = News
    # Используем другой шаблон — article.html
    template_name = 'article.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'article'


# Добавляем новое представление для создания новостей.
class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель новостей
    model = News
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'

    def create_product(request):
        form = NewsForm()

        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():

                i = form.cleaned_data

                f = News(
                      name=i['name'],
                      description=i['description'],
                      category=i['category'],
                 )
                f.save()
                return HttpResponseRedirect('/products/')

        return render(request, 'product_edit.html', {'form': form})

class NewsSearch(ListView):
    model = News
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10
    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }
# Добавляем представление для изменения товара.
class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

# Представление удаляющее товар.
class NewsDelete(DeleteView):
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
