
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/<str:username>", views.new_post, name="new_post"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('following', views.following, name="following"),
    path('follow/<str:username>', views.follow, name="follow"),
    path('unfollow/<str:username>', views.unfollow, name="unfollow"),
    path('edit/<int:post_id>', views.edit, name="edit_post"),
    path('like/<int:post_id>', views.like, name="like"),
    path('unlike/<int:post_id>', views.unlike, name="unlike")
]
