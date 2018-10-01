from django.urls import path

from . import views

from .views import (
        Home,
        PostCreateView,
        post_edit,
        PostDetailView,
        CommentView
    )

app_name = 'coffee'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post-edit'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/comment/', CommentView.as_view(), name='comment'),
]
