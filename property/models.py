from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
from account.models import Landlord, Agent
import uuid 


# Property information
class Apartment(models.Model):
    name = models.CharField("Name", max_length=50)
    location = models.CharField("Location", max_length=100)
    geom = models.PointField(srid=4326)
    units = models.IntegerField("No of Units")
    owner = models.ForeignKey(Landlord, related_name="landlord", on_delete=models.CASCADE)
    house_types = models.CharField("House Types", max_length=120)
    occupied_units = models.IntegerField("Occupied Units", default=0)
    apartment_image = models.ImageField(upload_to="apartments/%Y/", default="apartment.jpg", blank=True)
    slug = models.SlugField(blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "Apartment"
        verbose_name_plural = "Apartments"

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        size = (763, 508)
        img = Image.open(self.apartment_image)
        if img.height > 508 or img.width > 763:
            img.thumbnail(size)
            img.save(self.apartment_image.path)

    def get_empty_units(self):
        return self.units - self.occupied_units

    # def get_absolute_url(self):
    #     return reverse("Apartment_detail", kwargs={"pk": self.pk})


# Create your models here.
class Property(models.Model):
    PROPERTY = (
        ('Rental'),
        ('Sales'),
    )

    HOUSE_TYPE = (
        ('Single Rooms', 'Single Rooms'),
        ('Bed Sitter', 'Bed Sitter'),
        ('One Bedroom', 'One Bedroom'),
        ('Two Bedroom', 'Two Bedroom'),
        ('Three Bedroom', 'Three Bedroom'),
        ('Four Bedroom', 'Four Bedroom'),
        ('Five Bedroom', 'Five Bedroom'),
    )

    BATHROOM = (
        ('1', '1 Baths'),
        ('2', '2 Baths'),
        ('3', '3 Baths')
    )

    HOME_TYPE = (
        ('Buy', 'Buy'),
        ('Rent', 'Rent'),
        ('Sold', 'Sold')
    )

    title = models.CharField("Title", max_length=250)
    description = models.TextField("Description")
    location = models.CharField("Location", max_length=150)
    geom = models.PointField("")
    property_type = models.CharField("Property Type", max_length=50, choices=HOUSE_TYPE)
    price = models.IntegerField("Price")
    year_built = models.DateField("Year Built", auto_now=False, auto_now_add=False)
    beds = models.IntegerField("Beds", default=1)
    baths = models.IntegerField("Baths", default=1)
    square_feet = models.IntegerField("Square Feet")
    is_furnished = models.BooleanField('Furnished', default=False)
    slug = models.SlugField("Slug Field", blank=True)
    posted = models.DateTimeField("Posted", auto_now=True)
    is_occupied = models.BooleanField("Occupied", default=False)
    apartment = models.ForeignKey(Apartment, related_name="apartment", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

    # def get_absolute_url(self):
    #     return reverse("Property_detail", kwargs={"pk": self.pk})

class PropertyImage(models.Model):
    house = models.ForeignKey(Property, related_name="property", on_delete=models.CASCADE)
    image = models.ImageField("image", upload_to="property/%Y", default="/property/grayscale.jpg")

    class Meta:
        verbose_name = "Property Image"
        verbose_name_plural = "Property Images"

    def __str__(self):
        return self.house.title

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        size = (763, 508)
        img = Image.open(self.image)
        if img.height > 508 or img.width > 763:
             img.thumbnail(size)
             img.save(self.image.path)

    # def get_absolute_url(self):
    #     return reverse("Image_detail", kwargs={"pk": self.pk})

# tenants model
class Tenants(models.Model):
    HOUSE_TYPE = (
        ('Single Rooms', 'Single Rooms'),
        ('Bed Sitter', 'Bed Sitter'),
        ('One Bedroom', 'One Bedroom'),
        ('Two Bedroom', 'Two Bedroom'),
        ('Three Bedroom', 'Three Bedroom'),
        ('Four Bedroom', 'Four Bedroom'),
        ('Five Bedroom', 'Five Bedroom'),
    )

    MARITAL_STATUS = (
        ('Single', 'Single'),
        ('Married', 'Married')
    )

    first_name = models.CharField("First Name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50)
    id_number = models.IntegerField("ID Number")
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    room_code = models.CharField("Room Code", max_length=20)
    floor = models.IntegerField("Floor", default=0)
    phone_number = models.CharField("Phone Number", max_length=13)
    email = models.EmailField("Email Address", blank=True)
    marital_status = models.CharField("Marital Status", max_length=50, choices=MARITAL_STATUS)  
    room_type = models.CharField("Room Type", max_length=50, choices=HOUSE_TYPE)
    is_active = models.BooleanField("Active Tenant")
    geom = models.PointField(srid=4326)
    is_paid = models.BooleanField(default=False)
    rent_charge = models.IntegerField(default=10000)

    class Meta:
        verbose_name = "Tenants"
        verbose_name_plural = "Tenants"

    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    # def get_absolute_url(self):
    #     return reverse("Tenants_detail", kwargs={"pk": self.pk})

class RentPayment(models.Model):
    PAYMENT_MODE = (
        ("MPESA","M-PESA"),
        ("CASH", "CASH"),
        ("BANK", "BANK")
    )

    receipt_number = models.CharField(blank=True, max_length=8, unique=True)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    amount_paid = models.IntegerField("Amount Paid")
    paid_on = models.DateTimeField("Payment Date", auto_now=True)
    payment_mode = models.CharField("Payment Mode", max_length=50, choices=PAYMENT_MODE)
    receipt = models.ImageField("Receipt", upload_to="reciepts/%Y/%M/")

    class Meta:
        verbose_name = "RentPayment"
        verbose_name_plural = "RentPayments"

    def __str__(self):
        return self.receipt_number

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("RentPayment_detail", kwargs={"pk": self.pk})
    
