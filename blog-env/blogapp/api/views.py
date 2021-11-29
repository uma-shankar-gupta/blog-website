from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from blogapp.models import Post, Like
from .serializers import PostSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly,IsAuthenticated
from django.http import JsonResponse
from .cp import IsOwnerOrReadOnly, IsOwner
from knox.auth import TokenAuthentication



class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class= PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
class UserViewSet(CreateAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes = [AllowAny]
    
class UserEdit(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsOwner]
 
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def like(request):
    print(request.data)
    post = Post.objects.get(id=int(request.data['post_id']))
    has_liked = Like.objects.filter(for_post=post, like_by=request.user)

    if  has_liked:
        has_liked.delete()
    else:
        liked =Like(for_post=post, like_by=request.user)
        liked.save()
    data = {
            'like_count':Like.objects.filter(for_post=post).count(),
        }
    return JsonResponse(data)
   