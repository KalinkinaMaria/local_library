import uuid

from django.db import models
from django.urls import reverse

# Create your models here.

LOAN_STATUS = (
    ('m', 'Maintenance'),
    ('o', 'On loan'),
    ('a', 'Available'),
    ('r', 'Reserved'),
)


class BookLanguage(models.Model):
    """
    Модель языка книги
    """
    name = models.CharField(max_length=100, help_text="Введите язык")
    
    def __str__(self):
        """
        Представление модели в виде строки
        """
        return self.name


class BookGenre(models.Model):
    """
    Модель книжного жанра
    """
    name = models.CharField(max_length=200, help_text="Введите жанр книги")
    
    def __str__(self):
        """
        Представление модели в виде строки
        """
        return self.name


class Author(models.Model):
    """
    Модель автора
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Умер', null=True, blank=True)
    
    def get_absolute_url(self):
        """
        Возвращает URL для доступа к конкретного автора.
        """
        return reverse('author-detail', args=[str(self.id)])
    

    def __str__(self):
        """
        Представление модели в виде строки
        """
        return f"{self.first_name} {self.last_name}"
    

    def str_for_list_view(self):
        return f"{self.first_name} {self.last_name} {self.str_date()}"
    

    def str_date(self):
        return f"({self.date_of_birth} - {self.date_of_death if not self.date_of_death is None else ''})" 


class Book(models.Model):
    """
    Модель книги
    """
    title = models.CharField(max_length=200)
    author = models.ManyToManyField(Author, help_text="Выбрать автора")
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(BookGenre, help_text="Выбрать жанр")
    language = models.ManyToManyField(BookLanguage, help_text="Выбрать язык")
    
    def __str__(self):
        """
        Представление модели в виде строки
        """
        return self.title
    
    
    def get_absolute_url(self):
        """
        Возвращает URL для доступа к конкретной книге.
        """
        return reverse('book-detail', args=[str(self.id)])


    def display_author(self):
        """
        Создать строковое представление для авторов. Ипользуется для отображения авторов в админке.
        """
        authors = self.author.all()
        print(authors)
        return ', '.join([str(author) for author in authors[:3]]) + (', ...' if len(authors) > 3 else '')
    display_author.short_description = 'Author'


    def display_genre(self):
        """
        Создать строковое представление для жанра. Ипользуется для отображения жанра в админке.
        """
        genres = self.genre.all()
        return ', '.join([genre.name for genre in genres[:3]]) + (', ...' if len(genres) > 3 else '')
    display_genre.short_description = 'Genre'


    def count_instanses(self):
        return len(self.bookinstance_set.all())


class BookInstance(models.Model):
    """
    Модель экземпляра книги
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID для конкретного экземпляра книги в данной библиотеке")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Доступность книги')

    class Meta:
        ordering = ["due_back"]
        

    def __str__(self):
        """
        String for representing the Model object
        """
        return f"{self.id} ({self.book.title})"
