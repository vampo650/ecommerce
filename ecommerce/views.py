__author__ = 'vamsi'

from catalogue.models import Book
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """
        This function is not using in this sample project,
         because frontend has been integrated with AngularJS.
        :param kwargs:
        :return:
        """
        context = super(Home, self).get_context_data(**kwargs)
        context['books'] = Book.objects.get_books()
        return context
