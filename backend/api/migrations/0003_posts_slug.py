# Generated by Django 4.0.6 on 2022-07-05 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_posts_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='slug',
            field=models.SlugField(editable=False, max_length=200, null=True, unique=True),
        ),
    ]