# Generated by Django 4.0.6 on 2022-07-06 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_posts_email_publisher_alter_posts_dislikes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='likes',
        ),
    ]
