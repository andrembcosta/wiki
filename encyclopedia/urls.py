from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random_page", views.random_page, name="random_page"),
    path("wiki/<str:entry_name>", views.load_entry, name="entry"),
    path("create", views.create_page, name="create"),
    path("wiki/<str:entry_name>/edit", views.edit_page, name="edit"),
    path("error_create", views.error_creating_page, name="error_create"),
    path("search", views.search, name="search")
]
