from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:book_id>/', views.DetailView.as_view(), name='detail'),

    path('create/', views.animal_create, name='create'),
    path('<int:author_id>/', views.detail, name='detail'),
    path('authors/', views.authors, name='authors'),
    path('create_author/', views.create_author, name='create_author'),
]


