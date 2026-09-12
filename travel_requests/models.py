from django.db import models


class TravelRequest(models.Model):

    PURPOSE_CHOICES = [
        ('Leisure',  'Leisure'),
        ('Business', 'Business'),
        ('Umrah',    'Umrah'),
        ('Hajj',     'Hajj'),
        ('Medical',  'Medical'),
        ('Other',    'Other'),
    ]

    full_name          = models.CharField(max_length=255)
    email              = models.EmailField()
    phone_number       = models.CharField(max_length=20)
    destination        = models.CharField(max_length=255)
    number_of_travelers = models.PositiveIntegerField()
    travel_date        = models.DateField()
    travel_purpose     = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    body               = models.TextField()
    created_at         = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} — {self.destination}"