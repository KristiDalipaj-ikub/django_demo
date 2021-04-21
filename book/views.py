from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from book.models import Book, Animal, Author, Genre, Language


def animal_create(request):
    animal_name = request.data.name
    animal_nr_feet = request.data.nr_feet

    Animal.objects.create(animal_name=animal_name, nr_feet=animal_nr_feet)


def book_index(request):
    """
    Me lexo sa libra kam, ose
    Me lexo sa libra kam ne sistem,
    Me lexo librat qe kane nje usht te caktuar
    :param request:
    :return:
    """

    books = Book.objects.all()
    authors = Author.objects.all()
    context = {
        'books': books,
        'author': authors,
    }
    return render(request, 'book.template.book.index.html', context)


def book_detail(request, book_id):
    try:
        active_book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponse("Book does not exist")
    context = {
        "active_book": active_book
    }

    return render(request, "detail.html", context=context)


def detail(request, book_id):
    try:
        active_book = Book.objects.get(id=book_id)

    except Book.DoesNotExist:
        # raise Http404("Book does not exist. Try with another id")
        return HttpResponse("Book does not exist.Try with another id")
    return HttpResponse(active_book.book_info())


class BookForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    summary = forms.CharField(label='summary', max_length=1000)
    price = forms.CharField(label='price', max_length=10)


def test(request):
    print("ENTERED", request.method)
    if request.method == 'POST':

        form = BookForm(request.POST)
        if form.is_valid():
            data = form.data
            new_data = {
                'title': data['title'],
                'summary': data['summary'],
                'price': int(data['price']),
                'is_in_storage': True,
                'imprint': "test",
                'ISBN': "test",
                'qty': 241,
                'author': Author.objects.last(),
                'genre': Genre.objects.last(),
                'language': Language.objects.last(),
                'text_field': "test"
            }
            Book.objects.create(**new_data)

            return HttpResponse('Book created')
    else:
        form = BookForm()
    return render(request, 'create.html', {'form': form})


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
