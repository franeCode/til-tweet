from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField


class CodingStack(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = ImageField(upload_to='profiles/', default='profiles/no-image.jpeg', blank=True, null=True)
    cover = ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.CharField(max_length=150, blank=True, null=True, default='Default bio')
    name = models.CharField(max_length=50, blank=True, null=True, default='Full name')
    coding_stack = models.ManyToManyField(CodingStack, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a new Profile() object when a Django User is created."""
    
    if created:
        Profile.objects.create(user=instance)
        
        

