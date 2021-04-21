from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from datetime import date

# Create your models here.

"""
Charfield - string
DateField - Date
DateTimeField - Date Time 
Boolean - represents a boolean field
"""


class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(blank=True, null=True)

    def get_books_written_by_author(self):
        return self.book_set.all(), self.book_set.count()


class Genre(models.Model):
    parent_genre = models.ForeignKey("Genre", blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=20)


class Language(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)
    imprint = models.CharField(max_length=20)
    ISBN = models.CharField(max_length=30)
    is_in_storage = models.BooleanField()
    price = models.FloatField()
    qty = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    text_field = models.CharField(max_length=10)

    @staticmethod
    def cnt():
        return Book.objects.all().count()

    def book_info(self):
        return f"Book written from {self.author.name} is in our library. This book is written in {self.language.name}"


class BBBB(models.Model):
    year = models.DateField()


class Family(models.Model):
    name = models.CharField(max_length=100)
    a = models.ForeignKey(BBBB, on_delete=models.CASCADE, null=True)


class Animal(models.Model):
    """
    emri - string
	ngjyra - string
	nr_kembeve - integer
	familja - zvarranik, gjitar, amfib  - Lidhje me tabele
	vaksinuar - po / jo - boolean
	mosha - integer
	vizita_fundit - date
    """

    NGJYRAT = (
        ('kuqe', 'Kuqe'),
        ('blu', 'Blu'),
        ('bardhe', 'Bardhe')
    )

    name = models.CharField(max_length=100)
    color = models.CharField(choices=NGJYRAT, max_length=100)
    nr_feet = models.IntegerField(default=4)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    vaccinated = models.BooleanField(default=False)
    age = models.IntegerField()
    last_visit = models.DateField(default=date(2020, 1, 1))

    def is_due_for_checkup(self):
        if (timezone.now().date() - self.last_visit).days > 90:
            return "Due for a checkup"

    def __str__(self):
        return f"{self.name} {self.age}"


def generate_data():
    data = ['gjitar', 'amfib', 'peshq']
    f1 = open('data.txt')
    for row in f1:
        family = {}
        family['name'] = row.strip()
        Family.objects.create(**family)

    f2 = open('animal_data.txt')

    for row in f2:
        animal = {}
        split_data = row.split(',')
        animal['name'] = split_data[0]
        animal['color'] = split_data[1]
        animal['nr_feet'] = split_data[2]

        """....."""""

        Animal.objects.create(**animal)
