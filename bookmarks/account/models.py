from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Contact model to represent relationships between users
# This will be used for friend requests or following functionality 
class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
    def __str__(self):
        return f"{self.user_from} -> {self.user_to}"
    
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField(
    'self',through=Contact,
    related_name='followers',
    symmetrical=False
    )
)