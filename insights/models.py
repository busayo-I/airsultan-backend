from django.db import models


class Category(models.Model):
    name       = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering  = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Article(models.Model):

    STATUS_CHOICES = [
        ('Active',   'Active'),
        ('Inactive', 'Inactive'),
    ]

    title        = models.CharField(max_length=255)
    category     = models.ForeignKey(
                        Category,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='articles'
                    )
    body         = models.TextField()
    banner_image = models.ImageField(upload_to='insights/banners/')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title