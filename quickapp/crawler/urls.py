from django.urls import path

from . import views

urlpatterns = [
    path('get_one_information/', views.get_one_information, name='get_one_information'),
    path('get_one/', views.get_one, name='get_one'),
    path('get_random_poem/', views.get_random_poem, name='get_random_poem'),
]