from django.db import models
from django.contrib.auth.models import AbstractUser

from PIL import Image

# Create your models here.
class User(AbstractUser):
    is_agency = models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)
    date_joined = models.DateTimeField("Date Joined", auto_now=True)
    phone_number = models.CharField("Phone Number", max_length=13)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

# class landlord
class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Landlord"
        verbose_name_plural = "Landlords"

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("Landlord_detail", kwargs={"pk": self.pk})

# Roles models
# class Roles
# Contacts Model
class Contact(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    phone_number = models.CharField("Phone Number", max_length=13)
    email = models.EmailField("Email", max_length=254)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.user.username
    # def get_absolute_url(self):
    #     return reverse("Contact_detail", kwargs={"pk": self.pk})

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField("Profile Picture", upload_to="profile_picture", default="user.png")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.image.path)

        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)

