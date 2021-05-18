from django.db import models
from django.db.models.fields import EmailField


class Contact(models.Model):
    
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
