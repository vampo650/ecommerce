__author__ = 'vamsi'

from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from catalogue.models import Book, Author
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from catalogue.api.serializers import CatalogueSerializer, CatalogueDetailSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        """
        For this sample application, we are skipping csrf.
        :param request:
        :return:
        """
        return


class BookMixin:
    @staticmethod
    def change_author_datatype(input_request):
        """
        Changing author datatype i.e. list to list of dicts
        :param input_request: dict
        :return: dict
        """
        input_request['author'] = [{'name': data} for data in input_request['author']]
        return input_request


class CatalogueList(BookMixin, APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer = CatalogueSerializer

    def get(self, request):
        """
        Get all the books
        :param request:
        :return: list of dicts
        """
        try:
            response = self.serializer(Book.objects.get_books(), many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(err.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Creates a book
        :param request: dict
        :return: dict
        """
        try:
            data = BookMixin.change_author_datatype(request.data)
            serializer = self.serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(err.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CatalogueDetail(BookMixin, APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer = CatalogueDetailSerializer

    def put(self, request, catalogue_id):
        """
        Updates a book
        :param request: dict
        :param catalogue_id: int
        :return: dict
        """
        try:
            snippet = Book.objects.get_book(catalogue_id)
            data = BookMixin.change_author_datatype(request.data)
            serializer = self.serializer(snippet, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            return Response(err.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, catalogue_id):
        """
        Deletes a book
        :param request:
        :param catalogue_id: int
        :return: None
        """
        try:
            snippet = Book.objects.get_book(catalogue_id)
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response(err.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
