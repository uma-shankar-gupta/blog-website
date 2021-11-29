from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from blogapp.models import Post
from .serializers import PostSerializer

class PostListView(ListAPIView):
    queryset = Post.objects.all()[:10]
    serializer_class= PostSerializer

class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
