from django.db import models


class Offer(models.Model):

    TYPE_CHOICES = [
        ('Flights',  'Flights'),
        ('Hotels',   'Hotels'),
        ('Packages', 'Packages'),
    ]

    STATUS_CHOICES = [
        ('Active',   'Active'),
        ('Inactive', 'Inactive'),
    ]

    title        = models.CharField(max_length=255)
    type         = models.CharField(max_length=50, choices=TYPE_CHOICES)
    provider     = models.CharField(max_length=255)
    duration     = models.CharField(max_length=100)
    price        = models.DecimalField(max_digits=12, decimal_places=2)
    banner_image = models.ImageField(upload_to='offers/banners/')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title