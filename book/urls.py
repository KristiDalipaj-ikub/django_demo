from django.urls import path

from . import views

urlpatterns = [
    path('', views.book_index, name='index'),
    path('test/', views.test, name='book_create'),
    path('new_form/', views.test, name='new_test'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('create/', views.animal_create, name='create'),
    path('<int:author_id>/', views.detail, name='detail'),
    path('authors/', views.authors, name='authors'),
    path('create_author/', views.create_author, name='create_author'),
]


