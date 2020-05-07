from django.shortcuts import render
from django.views import generic

from . import models


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    num_books = models.Book.objects.all().count()
    num_instances = models.BookInstance.objects.all().count()

    num_instances_available = models.BookInstance.objects.filter(status__exact='a').count()
    num_authors = models.Author.objects.count()
    
    # Отрисовка HTML-шаблона index.html с данными внутри 
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors
        },
    )


class BookListView(generic.ListView):
    model = models.Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = models.Book


class AuthorListView(generic.ListView):
    model = models.Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = models.Author