from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Ruta vacía asociada a la vista index
]
