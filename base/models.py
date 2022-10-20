from email.policy import default
from winreg import REG_QWORD_LITTLE_ENDIAN
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Note(models.Model):
  sender = models.ForeignKey(User, related_name='message_sender', on_delete=models.CASCADE)
  receiver = models.ForeignKey(User, related_name='message_receiver', on_delete=models.CASCADE)
  content = models.TextField()
  created_at = models.DateTimeField(default=now, editable=False)
  readByReceiver = models.BooleanField(default=False)