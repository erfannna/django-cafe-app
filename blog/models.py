from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=100,
                             blank=False)
    short = models.CharField(max_length=250)
    content = models.TextField(blank=False)
    slug = models.SlugField(max_length=120)
    image = models.ImageField(upload_to='blog/images/%Y/%m/%d/',
                              blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    duration = models.PositiveIntegerField(default=5)
    archived = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[self.slug])

    def __str__(self):
        return str(self.title)
