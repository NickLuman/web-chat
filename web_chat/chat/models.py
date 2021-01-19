from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
 
class Chat(models.Model):
    members = models.ManyToManyField(User)
    check_sum = models.IntegerField()
    
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    is_readed = models.BooleanField(default=False)
    
    class Meta:
        ordering=['pub_date']
 
    def __str__(self):
        return self.message