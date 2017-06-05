__author__ = 'vamsi'

from django.db import models


class AuthorManager(models.Manager):
    def get_or_create_author(self, name):
        """
        Creates a author, if it doesn't exist
        :param name: string
        :return: object
        """
        author, created = self.get_or_create(name=name)
        return author


class Author(models.Model):
    name = models.CharField(
        max_length=255,
        help_text='Author Name'
    )
    created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        help_text='Author created on date'
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text='Author updated on date'
    )

    def __str__(self):
        return self.name

    __unicode__ = __str__

    objects = AuthorManager()


class BookManager(models.Manager):
    def create_book(self, title, description, authors):
        """
        Creates a book
        :param title: string
        :param description: string
        :param authors: objects
        :return: object
        """
        book = super(BookManager, self).create(title=title,
                                               description=description,
                                               )
        book.save()
        book.author.add(*authors)
        return book

    def get_books(self):
        """
        Get all the books
        :return: QuerySet
        """
        return self.all()

    def get_book(self, id):
        """
        Get a book
        :param id: int
        :return: object
        """
        return self.get(pk=id)


class Book(models.Model):
    title = models.CharField(
        unique=True,
        max_length=255,
        help_text='Book Name'
    )
    description = models.TextField(
        help_text='Book Description'
    )
    author = models.ManyToManyField(
        Author,
        help_text='Book Author',
    )
    created = models.DateTimeField(
        auto_now=False,
        auto_now_add=True,
        help_text='Book created on date'
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text='Book updated on date'
    )

    def __str__(self):
        return self.title

    __unicode__ = __str__

    def authors(self):
        """
        This function is exclusively for django admin.
        :return: string
        """
        return ", ".join([str(author) for author in self.author.all() if author])

    objects = BookManager()
