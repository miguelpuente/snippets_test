from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from pygments.lexers import get_all_lexers

# Obtener los nombres de los lenguajes soportados por Pygments
LEXERS = [(lexer[1][0], lexer[0]) for lexer in get_all_lexers() if lexer[1]]

class Language(models.Model):
    name = models.CharField(max_length=50, choices=LEXERS, unique=True)
    slug = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Language.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Snippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    snippet = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
