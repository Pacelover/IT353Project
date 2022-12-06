# Generated by Django 4.1.3 on 2022-12-05 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('isCompleted', models.BooleanField(default=False)),
            ],
        ),
    ]
