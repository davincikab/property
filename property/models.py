from django.contrib.gis.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image

# Create your models here.
class Property(models.Model):
    PROPERTY = (
        ('Rental'),
        ('Sales'),
    )

    BEDROOMS = (
        (0, 'Bed Sitter'),
        (1, 'One Bedroom'),
        (2, 'Two Bedroom'),
        (3, 'Three Bedroom'),
        (4, 'Four Bedroom'),
        (5, 'Five Bedroom'),
    )

    BATHROOM = (
        (1, '1 Baths'),
        (2, '2 Baths'),
        (3, '3 Baths')
    )

    HOME_TYPE = (
        ('Buy', 'Buy'),
        ('Rent', 'Rent'),
        ('Sold', 'Sold')
    )

    title = models.CharField("Title", max_length=70)
    description = models.TextField("Description")
    location = models.CharField("Location", max_length=150)
    geom = models.PointField("")
    property_type = models.CharField("Property Type", max_length=50)
    price = models.IntegerField("Price")
    year_built = models.DateField("Year Built", auto_now=False, auto_now_add=False)
    beds = models.CharField("Beds",  max_length=50, choices=BEDROOMS)
    baths = models.CharField("Beds",  max_length=50, choices=BATHROOM)
    square_feet = models.IntegerField("Square Feet")
    is_furnished = models.BooleanField('Furnished', default=False)
    slug = models.SlugField("Slug Field")
    posted = models.DateTimeField("Posted", auto_now=True)

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
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField("image", upload_to="property/%Y", default="/property/grayscale.jpg")

    class Meta:
        verbose_name = "Property Image"
        verbose_name_plural = "Property Images"

    def __str__(self):
        return self.property.name

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)

        size = (763, 508)
        img = Image.open(self.image)
        if img.height > 508 or img.width > 763:
             img.thumbnail(size)
             img.save(self.image.path)

    # def get_absolute_url(self):
    #     return reverse("Image_detail", kwargs={"pk": self.pk})


# Property information
