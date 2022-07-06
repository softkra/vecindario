"""vecindario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import PostsList, PostsCreate, PostsDetails, LikesIncrement, DislikesIncrement, CreateUser, NotificationsList, ProfileData

urlpatterns = [
    path('authentication/', include('dj_rest_auth.urls')),
    path('registration/',CreateUser.as_view(),name='add-user'),
    path('', PostsList.as_view(), name='home'),
    path('posts/add/', PostsCreate.as_view(), name='post-create'),
    path('posts/', PostsDetails.as_view(), name='post-details'),
    path('like/<uuid:pk>/', LikesIncrement.as_view(), name='like-increment'),
    path('dislike/<uuid:pk>/', DislikesIncrement.as_view(), name='dislike-increment'),
    path('notifications/', NotificationsList.as_view(), name='notifications-list'),
    path('profile/', ProfileData.as_view(), name='profile'),
]


