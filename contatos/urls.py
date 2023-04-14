from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('<int:contato.id>', views.index, name='index'),
]
