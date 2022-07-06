from django.contrib import admin
from .models import Posts, Notifications, Reactions
# Register your models here.

class PostsAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    list_display = ('id', 'name', 'slug', 'likes', 'dislikes')
admin.site.register(Posts, PostsAdmin)

class NotificationsAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    list_display = ('id', 'message', 'created')
admin.site.register(Notifications, NotificationsAdmin)

class ReactionsAdmin(admin.ModelAdmin):
    list_filter = ('created',)
    list_display = ('id', 'post', 'user', 'like', 'dislike', 'is_removed')
admin.site.register(Reactions, ReactionsAdmin)