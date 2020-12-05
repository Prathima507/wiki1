from django.urls import path,include
from django.contrib import admin

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create", views.create, name="create"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki", views.randomPage, name="randomPage")
]
