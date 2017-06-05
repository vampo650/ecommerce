__author__ = 'vamsi'

from django.test import TestCase
from catalogue.models import Book, Author


class BookTestCase(TestCase):
    def setUp(self):
        """
        Creates a book
        """
        self.data = {"title": "C++", "description": "Programming Language"}
        author = Author.objects.get_or_create_author("Bjarne Stroustrup")
        self.data["authors"] = [author]
        book = Book.objects.create_book(**self.data)
        self.book_id = book.pk

    def test_author_records_count(self):
        """
        Checks Author Records
        """
        self.assertEqual(Author.objects.count(), 1)

    def test_check_book_description(self):
        """
        Checks Book Description
        """
        book = Book.objects.get_book(self.book_id)
        self.assertEqual(book.description, "Programming Language")
