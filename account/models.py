from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_agency = models.BooleanField(default=False)
    is_landlord = models.BooleanField(default=False)
    phone_number = models.CharField("Phone Number", max_length=13)

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
