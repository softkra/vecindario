from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel
from django.utils.translation import gettext as _
import uuid
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import random
# Create your models here.

class Posts(SoftDeletableModel, TimeStampedModel):

    """Model for managing Posts

    Attributes:
        name: Posts name
        body: Posts body
        likes: Posts counter likes
        dislikes: Posts counter dislikes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length = 200, unique=True, editable=False, null=True)
    body = models.TextField()
    email_publisher = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuario Creador"
    )

    def save(self, *args, **kwargs):
        to_slug = slugify(self.name)
        if Posts.objects.filter(slug=to_slug).exists():
            name_slug = self.name, random.randint(0, 9)
            to_slug = slugify(name_slug)
        self.slug = slugify(to_slug)
        if not self.email_publisher:
            self.email_publisher = self.user.email
        super(Posts, self).save(*args, **kwargs)
    
    @property
    def likes(self):
        return Reactions.objects.filter(post=self.id, like=True).count()
    
    @property
    def dislikes(self):
        return Reactions.objects.filter(post=self.id, dislike=True).count()
    
    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Posts'
        verbose_name_plural = 'Posts'
        default_permissions = ()

class Reactions(SoftDeletableModel, TimeStampedModel):

    """Model for managing Reactions

    Attributes:
        like: Reactions like
        dislike: Reactions dislike
        user: user reaction
        post: Post ID
    """
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuario que reacciona"
    )
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        verbose_name="Post ID"
    )

    class Meta:
        verbose_name = 'Reactions'
        verbose_name_plural = 'Reactions'
        default_permissions = ()

@receiver(post_save, sender=Reactions)
def create_notification(sender, instance, created, **kwargs):
    if created:
        try:
            post = Posts.objects.get(pk=instance.post.id)
            notification = Notifications(
                post = post,
                message = f'El usuario {instance.user.username} ha reaccionado a tu post {instance.post.name}'
            )
            notification.save()
        except Posts.DoesNotExist:
                ...

# @receiver(post_delete, sender=Reactions)
# def decrease_reaction_post(sender, instance, *args, **kwargs):
#     print("Se va a eliminar un like")
#     if instance.like == True:
#         post = Posts.objects.get(pk=instance.post.id)
#         post.likes = post.likes - 1
#         post.save()
#     if instance.dislike == True:
#         post = Posts.objects.get(pk=instance.post.id)
#         post.likes = post.dislikes - 1
#         post.save()
    
class Notifications(SoftDeletableModel, TimeStampedModel):

    """Model for managing Notifications

    Attributes:
        message: Message to notify
        post: Post ID
    """
    message = models.TextField()
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        verbose_name="Post"
    )

    class Meta:
        verbose_name = 'Notifications'
        verbose_name_plural = 'Notifications'
        default_permissions = ()