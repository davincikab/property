from django.dispatch import receiver
from django.db.models.signals import post_save


from .models import User, UserProfile, Landlord

@receiver(post_save, sender=User)
def create_pprofile(sender, instance, created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

        if instance.is_agency:
            # create agency instance
            Agent.objects.create(user=instance)
        
        if instance.is_landlord:
            # create lanlord instance
            Landlord.objects.create(user=instance)