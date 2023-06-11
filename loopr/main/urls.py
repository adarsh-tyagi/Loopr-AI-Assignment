from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("newbook", views.create_book, name="create_book"),
    path("searchbook", views.search_book, name="search_book"),
    path("issuebook", views.issue_book, name="issue_book"),
    path("returnbook", views.return_book, name="return_book"),
    path("deleteuser", views.delete_user, name="delete_user"),
    path("deletebook", views.delete_book, name="delete_book"),
]
