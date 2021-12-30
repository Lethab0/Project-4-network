
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("AddPost", views.AddPost , name="AddPost"),
    path("Following/<str:action>/<int:ID>", views.Following , name="Following"),
    path("Followed_people", views.Followed_people , name="Followed_people"),
    path("Profile/<str:texter>", views.User_Profile , name="User_Profile"),

    #API routes
    path("liked/<int:ID>", views.liked_posts , name="liked_posts"),
    path("Edit_posts", views.Edit_post , name="Edit_post"),
    path("like_or_unlike/<int:ID>", views.like_or_unlike , name="like_or_unlike"),
    path("Edit/<int:ID>", views.Edit , name="Edit"),
    
]
