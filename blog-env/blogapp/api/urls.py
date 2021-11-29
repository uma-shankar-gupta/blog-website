from rest_framework.routers import DefaultRouter
from .views import PostViewSet, UserViewSet, UserEdit, like
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns =[
    path('', include('knox.urls')),
    path('register/', UserViewSet.as_view()),
    path('user/<int:pk>/', UserEdit.as_view()),
    path('like/', like)
] + router.urls
