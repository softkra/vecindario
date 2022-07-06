from django.shortcuts import render
from rest_framework.views import APIView
from .models import Notifications, Posts, Reactions
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostsSerializer, PostsCreateSerializer, UserSerializer, NotificationsSerializer
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError

# Create your views here.
""" MODULE: POSTS """

"""
    Class to list paginated posts and sorted by likes
"""
class PostsList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)
    def get(self, request):
        posts = sorted(Posts.objects.all(), key=lambda t: -t.likes)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostsSerializer(result_page, many=True, context={'request':request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

"""
    Class to create a post
"""
class PostsCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = get_user_by_token(request)
        serializer = PostsCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
    Class to GET or PUT a post by uuid
"""
class PostsDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    def get_queryset(self, pk):
        try:
            return Posts.objects.get(id=pk)
        except Posts.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        post = self.get_queryset(pk)
        serializer = PostsSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_queryset(pk)
        serializer = PostsSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
    Class to manage 'like' reaction
"""
class LikesIncrement(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            post = Posts.objects.get(id=pk)
            data = get_user_by_token(request)
            user_instance = User.objects.get(pk=data['user'])
            reaction_validate = Reactions.objects.filter(post=post, user=user_instance, like=True).exists()
            if not reaction_validate:
                reaction_created = Reactions.objects.create(
                    post = post,
                    user=user_instance,
                    like=True,
                    dislike=False
                )
                Reactions.objects.filter(post=post, user=user_instance).exclude(id=reaction_created.id).delete()
            else:
                Reactions.objects.filter(post=post, user=user_instance, like=True).delete()
            new_post = Posts.objects.get(id=pk)
            serializer = PostsSerializer(new_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Posts.DoesNotExist:
            return Response({"error":"Post invalid"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error":"User invalid"}, status=status.HTTP_404_NOT_FOUND)

"""
    Class to manage 'dislike' reaction
"""
class DislikesIncrement(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk):
        try:
            post = Posts.objects.get(id=pk)
            data = get_user_by_token(request)
            user_instance = User.objects.get(pk=data['user'])
            reaction_validate = Reactions.objects.filter(post=post, user=user_instance, dislike=True).exists()
            if not reaction_validate:
                reaction_created = Reactions.objects.create(
                    post = post,
                    user=user_instance,
                    like=False,
                    dislike=True
                )
                Reactions.objects.filter(post=post, user=user_instance).exclude(id=reaction_created.id).delete()
            else:
                Reactions.objects.filter(post=post, user=user_instance, dislike=True).delete()
            new_post = Posts.objects.get(id=pk)
            serializer = PostsSerializer(new_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Posts.DoesNotExist:
            return Response({"error":"Post invalid"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error":"User invalid"}, status=status.HTTP_404_NOT_FOUND)

""" MODULE: USER """

"""
    Class to create user system
"""
class CreateUser(APIView):
    serializer_class = None
    permission_classes = (AllowAny,)
    def post(self,request):
        """
            POST Method. Params: data: {
                username: Username,
                email: Email user (Optional),
                password: Password user,
                first_name: first_name user (Optional),
                last_name: last_name user (Optional)
            }
        """
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = User.objects.create_user(
                    request.data['username'],
                    request.data['email'],
                    request.data['password']
                )
                user.first_name = request.data['first_name']
                user.last_name = request.data['last_name']
                user.save()
                return Response("User added successfully", status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError:
            return Response("Error adding the user", status.HTTP_500_INTERNAL_SERVER_ERROR)
        except IntegrityError as e:
            print(e)
            return Response("Database error adding the user", status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
    Class to list notifications by user
"""
class NotificationsList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = get_user_by_token(request)
        posts = Notifications.objects.filter(post__user=user['user'])
        serializer = NotificationsSerializer(posts, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

"""
    Class to profile data
"""
class ProfileData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = get_user_by_token(request)
        user_data = User.objects.get(pk=user['user'])
        total_notifications = Notifications.objects.filter(post__user=user['user']).count()
        total_posts = Posts.objects.filter(user=user['user']).count()
        total_likes = Reactions.objects.filter(user=user['user'], like=True).count()
        total_dislikes = Reactions.objects.filter(user=user['user'], dislike=True).count()
        result = {
            "username":user_data.username,
            "first_name":user_data.first_name,
            "last_name":user_data.last_name,
            "email":user_data.email,
            "total_notifications":total_notifications,
            "total_posts":total_posts,
            "total_likes":total_likes,
            "total_dislikes":total_dislikes,
        }
        response = Response(result, status=status.HTTP_200_OK)
        return response


"""
    Funtion get user by token to interact with serializers
"""
def get_user_by_token(request):
    data = request.data
    if type(data) is dict:
        data['user'] = request.user.id
    else:
        mutable = data._mutable
        data._mutable = True
        data["user"] = request.user.id
        data._mutable = mutable
    return data