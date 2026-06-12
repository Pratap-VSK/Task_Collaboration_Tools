from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


COLOR_SCHEME_CHOICES = [
    ('blue', 'Blue'),
    ('purple', 'Purple'),
    ('green', 'Green'),
    ('orange', 'Orange'),
    ('pink', 'Pink'),
    ('indigo', 'Indigo'),
]

THEME_MODE_CHOICES = [
    ('light', 'Light Mode'),
    ('dark', 'Dark Mode'),
]

COLOR_HEX_MAP = {
    'blue': '#3B82F6',
    'purple': '#A855F7',
    'green': '#10B981',
    'orange': '#F59E0B',
    'pink': '#EC4899',
    'indigo': '#6366F1',
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    theme_mode = models.CharField(max_length=10, choices=THEME_MODE_CHOICES, default='light')
    color_scheme = models.CharField(max_length=10, choices=COLOR_SCHEME_CHOICES, default='blue')
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def color_hex(self):
        return COLOR_HEX_MAP.get(self.color_scheme, '#3B82F6')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
