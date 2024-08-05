
from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet
from django.conf import settings

# get current user model  
User=get_user_model()

# my ciphar
f = Fernet(settings.ENCRYPT_KEY)
class Conversation(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_conversations')
    participants=models.ManyToManyField(User, related_name="conversations")
    last_message_at=models.DateTimeField(default=timezone.now)
    is_seen=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        usernames=' ,'.join([user.username for user in self.participants.all()])
        return usernames
    
    class Meta:
        ordering = ['-last_message_at']

    def get_absolute_url(self):
        return f'/conversation/{self.id}'

class Message(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sent_messages')
    conversation=models.ForeignKey(Conversation, on_delete=models.CASCADE ,related_name='messages')
    body=models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def body_decrypted(self):
        # decrypt
        message_decrypted = f.decrypt(self.body)
        # from binary to string
        message_decoded = message_decrypted.decode('utf-8')
        return message_decoded

    def __str__(self):
        return f'{self.sender.username} : {self.body[:30]}' 
        
    class Meta:
        ordering = ['created']