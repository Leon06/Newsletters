import email
from pyexpat import model
from unicodedata import name
from django.db import models

#los usuarios que nos den su correo
class NewsletterUser(models.Model):
    email= models.EmailField(null=False, unique=True)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# Formato de Correos que queremos enviar

class Newsletter(models.Model):
    name=models.CharField(max_length=250)
    subject=models.CharField(max_length=250)
    body=models.TextField(blank=True, null=True)
    email = models.ManyToManyField(NewsletterUser) #A los correo que le queremos enviar los emails
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


