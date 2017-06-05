__author__ = 'vamsi'

from models import Author, Book
from django.contrib import admin


class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('title', 'description', 'authors', 'created', 'updated')
    list_filter = ('title', 'author', 'created', 'updated')
    ordering = ['-updated']


class AuthorAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('name', 'created', 'updated')
    list_filter = ('name', 'created', 'updated')
    ordering = ['-updated']


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
