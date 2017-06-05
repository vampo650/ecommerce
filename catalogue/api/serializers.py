__author__ = 'vamsi'

from django.http import Http404
from rest_framework import serializers
from catalogue.models import Book, Author
from rest_framework.exceptions import ValidationError


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        help_text='Author Name'
    )

    def create(self, validated_data):
        """
        Creates a author, if it doesn't exist
        """
        return Author.objects.get_or_create_author(validated_data['author'])


class CatalogueSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        help_text='Book Title'
    )
    description = serializers.CharField(
        required=True,
        help_text='Book Description'
    )
    author = AuthorSerializer(
        many=True,
        help_text='Book Author'
    )

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'author', 'created', 'updated')

    def create(self, validated_data):
        """
        Creates a book
        """
        author_list = [Author.objects.get_or_create_author(am['name']) for am in validated_data['author']]
        return Book.objects.create_book(validated_data['title'],
                                        validated_data['description'],
                                        author_list
                                        )


class CatalogueDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(
        required=False,
        many=True,
        help_text='Catalogue Author'
    )

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'author', 'created', 'updated')

    def update(self, instance, validated_data):
        """
        Updates a book
        """
        if validated_data.get('author', None):
            for author in instance.author.all():
                instance.author.remove(author)

            for author in validated_data['author']:
                instance.author.add(Author.objects.get_or_create_author(author['name']))

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
