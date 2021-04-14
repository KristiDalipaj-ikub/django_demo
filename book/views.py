from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, Http404

from book.models import Book, Animal, Author


def animal_create(request):
    animal_name = request.data.name
    animal_nr_feet = request.data.nr_feet

    Animal.objects.create(animal_name=animal_name, nr_feet=animal_nr_feet)


def index(request):
    """
    Me lexo sa libra kam, ose
    Me lexo sa libra kam ne sistem,
    Me lexo librat qe kane nje usht te caktuar
    :param request:
    :return:
    """
    data = []
    animals = Animal.objects.all()
    for animal in animals:
        data.append((animal.name, animal.last_visit))
    return HttpResponse(data)
    # return HttpResponse("Hello. You are accessing the books app."
    #                     "As of right now , we have book/s")


def detail(request, book_id):
    try:
        active_book = Book.objects.get(id=book_id)

    except Book.DoesNotExist:
        # raise Http404("Book does not exist. Try with another id")
        return HttpResponse("Book does not exist.Try with another id")
    return HttpResponse(active_book.book_info())


def authors(request):
    """
    Author.objects.order_by('-name')[:5]
    equivalent
    Author.objects.all().order_by('-name')[:5]
    """
    author_list_data = Author.objects.order_by('-name')[:5]
    return HttpResponse([author_data.name for author_data in author_list_data])


def create_author(request):
    name = request.body['name']
    surname = request.body['surname']

    a = Author.objects.create(name=name + surname)
    if a:
        return HttpResponse("AUTHOR CREATED NORMALLY")
    else:
        return HttpResponse("FAILED TO CREATE AUTHOR")


def author_name_for_given_book(request, book_id):
    book = Book.objects.get(id=book_id)
    return HttpResponse(f"Book with name {book.title} "
                        f"is written by {book.author.name}")

def books_written_by_author(request, author_id):
    author = Author.objects.get(id=author_id)
    books = author.book_set.all()
    return HttpResponse([book.name for book in books])

from django.views import generic


class IndexView(generic.ListView):
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Book.objects.order_by('-title')[:5]


class DetailView(generic.DetailView):
    model = Book
    # template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Book
    # template_name = 'polls/results.html'
