from django.urls import path
from . import views
from .views import (
    PostList,
    PostDetail,
    PostCreate,
    PostUpdate,
    PostDelete,
    UserList,
)

urlpatterns = [
    path('', PostList.as_view(), name='blog-home'),
    path('like/', views.like, name='like'),
    path('coment/', views.coment, name='coment'),
    path('search/', views.search, name='search'),
    path('register/validuser/', views.validate_username, name='validuser'),
    path('user/<str:username>', UserList.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('post/new/', PostCreate.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdate.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDelete.as_view(), name='post-delete'),
    path('about/', views.about, name='about')
]