from django.urls import path

from .views import *




urlpatterns = [
    path("", article_list_create_view, name="article-list"),
    path("<int:pk>/", article_detail_view, name="article-detail"),
    path("<int:pk>/update/", article_update_view, name="article-update"),       
    path("<int:pk>/delete/", article_destroy_view, name="article-delete"),
]