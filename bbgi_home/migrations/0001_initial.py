# Generated by Django 4.2.5 on 2024-10-27 14:38

import bbgi_home.utilities.file_handlers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, help_text='Upload news image.', null=True, upload_to=bbgi_home.utilities.file_handlers.handle_post_file_upload)),
                ('title', models.CharField(help_text='Enter title for your news', max_length=150)),
                ('description', models.CharField(help_text='Write a short description about this post', max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True)),
                ('content', tinymce.models.HTMLField()),
                ('author', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='category/')),
                ('slug', models.SlugField(max_length=350, unique=True)),
                ('label', models.CharField(max_length=250, unique=True)),
            ],
            options={
                'verbose_name': 'Categorie',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='EmailModel',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=70)),
                ('from_email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('message', models.TextField(max_length=500)),
                ('task_id', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('question', models.CharField(max_length=250)),
                ('answer', models.CharField(max_length=550)),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='home/images/team')),
                ('full_names', models.CharField(help_text='Enter member full names', max_length=250)),
                ('slug', models.SlugField(max_length=350)),
                ('role', models.CharField(help_text='Enter member role', max_length=250)),
                ('decription', tinymce.models.HTMLField(blank=True, help_text='Describe the team member', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(choices=[('Website Terms and Community Guidlines', 'Website Terms and Community Guidlines'), ('Refund Policy', 'Refund Policy'), ('Privacy Policy', 'Privacy Policy'), ('Terms of use: Consumers', 'Terms of use: Consumers'), ('Terms of use: Organisers', 'Terms of use: Organisers')], max_length=150, unique=True)),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('description', models.CharField(max_length=160)),
                ('content', tinymce.models.HTMLField()),
            ],
            options={
                'verbose_name': 'Privacy',
                'verbose_name_plural': 'Privacys',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
                ('commenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bbgi_home.blog')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='bbgi_home.blogcategory'),
        ),
    ]