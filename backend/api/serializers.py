from rest_framework import serializers
from .models import Posts, Notifications
from django.contrib.auth.models import User

class PostsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Posts
        fields = ('id', 'slug', 'name', 'email_publisher', 'username', 'likes', 'dislikes')

class PostsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('name', 'body', 'email_publisher', 'user')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'