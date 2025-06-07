from django.urls import path
from django_hausaufgabe_1.views import hello

urlpatterns =[
    path("hello/<str:name>/", view=hello,name="hello")
]