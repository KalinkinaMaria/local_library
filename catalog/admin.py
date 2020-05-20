from django.contrib import admin

from . import models


class BooksInline(admin.TabularInline):
    model = models.Book.author.through
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    #TODO почему отображается выпадающий список из BookInstance
    inlines = [BooksInline]

admin.site.register(models.Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = models.BookInstance
    extra = 0


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'display_genre')
    list_filter = ('author', 'genre', 'language')
    inlines = [BooksInstanceInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'summary')
        }),
        (None, {
            'fields': (('author', 'genre', 'language'), 'isbn')
        }),
    )


@admin.register(models.BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'imprint', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(models.BookGenre)
admin.site.register(models.BookLanguage)
