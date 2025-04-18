# Generated by Django 5.1.3 on 2024-12-06 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=200)),
                ('author', models.CharField(default='', max_length=200)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('content', models.FileField(upload_to='literature/')),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
