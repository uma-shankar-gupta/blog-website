from rest_framework import serializers
from blogapp.models import Post, Comment, Like
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password':{'write_only': True, 'required': True}}
        
    def create(self, data):
        user = User.objects.create_user(**data)
        return user
        

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['like_by']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)
    likes   = LikeSerializer(many=True, required=False)
    author = serializers.ReadOnlyField(source='author.username')
    image = serializers.ReadOnlyField(source='author.profile.image.url')
    class Meta:
        model = Post
        fields =['id', 'title', 'content', 'author','date_posted','likes', 'comments', 'image']
    