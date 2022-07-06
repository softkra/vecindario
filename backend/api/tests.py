import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import Posts, Notifications, Reactions
USER_DATA = {
    "username": "test_user_main",
    "email": "prueba@gmail.com",
    "password": "prueba123",
    "first_name": "Pepito",
    "last_name": "Perez",
}

USERS_DATA = [
    {
        "username": "test_user",
        "email": "prueba@gmail.com",
        "password": "prueba123",
        "first_name": "Pepito",
        "last_name": "Perez",
    },
    {
        "username": "test_user2",
        "email": "jaime@gmail.com",
        "password": "prueba123",
        "first_name": "Jaime",
        "last_name": "Perez",
    },
    {
        "username": "test_user3",
        "email": "roberto@gmail.com",
        "password": "prueba123",
        "first_name": "Roberto",
        "last_name": "Perez",
    }
]
class RegistrationUserTestCase(APITestCase):
    def test_registration(self):
        response = self.client.post("/api/registration/", USER_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USER_DATA["username"], password=USER_DATA["password"])

    def test_login(self):
        data = {
            "username":USER_DATA["username"], 
            "password":USER_DATA["password"]
        }
        response = self.client.post("/api/authentication/login/", data)
        token = Token.objects.filter(user=self.user).exists()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(True, token)

POSTS_DATA = {
    "name": "Backend developers",
    "body": "This is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large textThis is a large text",
    "email_publisher": "pepito@gmail.com" 
}
class PostsTestCase(APITestCase):
    def setUp(self):
        for row in USERS_DATA:
            self.user = User.objects.create_user(username=row["username"], password=row["password"])
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token))
        for i in range(20):
            post = Posts(
                name= f'{POSTS_DATA["name"]} {i}',
                body= POSTS_DATA["body"],
                email_publisher= POSTS_DATA["body"],
                user=self.user
            )
            post.save()

    def test_list_posts(self):
        response = self.client.get("/api/?page=1")
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 10)
    
    def test_list_posts_without_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get("/api/?page=1")
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 10)
    
    def test_create_post(self):
        response = self.client.post("/api/posts/add/", POSTS_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.post("/api/posts/add/", POSTS_DATA)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_increment_decrease_likes(self):
        post = Posts.objects.last()
        likes_counter = post.likes
        # Increment likes to post
        response = self.client.get(f"/api/like/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content.decode())
        self.assertEqual(int(data['likes']), (likes_counter+1))

        # Decrease likes if execute te function again
        response = self.client.get(f"/api/like/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content.decode())
        self.assertEqual(int(data['likes']), likes_counter)
    
    def test_increment_decrease_dislikes(self):
        post = Posts.objects.last()
        dislikes_counter = post.dislikes
        # Increment dislikes to post
        response = self.client.get(f"/api/dislike/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content.decode())
        self.assertEqual(int(data['dislikes']), (dislikes_counter+1))

        # Decrease dislikes if execute te function again
        response = self.client.get(f"/api/dislike/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content.decode())
        self.assertEqual(int(data['dislikes']), dislikes_counter)

class NotificationsTestCase(APITestCase):
    def setUp(self):
        # Create post user and a new post to react
        self.main_user = User.objects.create_user(username=USER_DATA["username"], password=USER_DATA["password"])
        self.main_token = Token.objects.create(user=self.main_user)
        self.post = Posts(
            name= POSTS_DATA["name"],
            body= POSTS_DATA["body"],
            email_publisher= POSTS_DATA["body"],
            user=self.main_user
        )
        self.post.save()
        # Create viewers (users)
        for row in USERS_DATA:
            user = User.objects.create_user(username=row["username"], password=row["password"])
            Token.objects.create(user=user)

    def test_get_notifications_by_likes(self):
        users = User.objects.filter().exclude(id=self.main_user.id)
        for row in users:
            token = Token.objects.get(user=row)
            self.client.credentials(HTTP_AUTHORIZATION="Token {}".format(token))
            response = self.client.get(f"/api/like/{self.post.id}/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        post_reactions = Posts.objects.get(pk=self.post.id)
        self.assertEqual(post_reactions.likes, len(USERS_DATA))

        notifications = Notifications.objects.filter(post=self.post.id).count()
        self.assertEqual(notifications, len(USERS_DATA))