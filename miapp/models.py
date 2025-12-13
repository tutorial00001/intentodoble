from django.db import models


class Practica(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    POST_TYPES = [
        ('discussion', 'Discussion'),
        ('question', 'Question'),
        ('review', 'Review'),
        ('news', 'News'),
    ]
    def can_edit(self, user):
        """Verifica si el usuario puede editar este post"""
        return self.author.id == user.id
    
    def can_delete(self, user):
        """Verifica si el usuario puede eliminar este post"""
        return self.author.id == user.id

    post_type = models.CharField(max_length=20, choices=POST_TYPES)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    author = models.ForeignKey(Practica, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
