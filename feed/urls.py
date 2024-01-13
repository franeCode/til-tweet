from django.urls import path 
from . import views

app_name = "feed"

urlpatterns = [
    path("", views.HomePage.as_view(), name="index"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("new/", views.CreateNewPost.as_view(), name="new_post"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path('post/<int:post_id>/comment/', views.CommentView.as_view(), name='create_comment'),
]

