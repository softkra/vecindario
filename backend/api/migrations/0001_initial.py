# Generated by Django 4.0.6 on 2022-07-05 14:35

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('likes', models.IntegerField()),
                ('dislikes', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Posts',
                'verbose_name_plural': 'Posts',
                'default_permissions': (),
            },
        ),
    ]