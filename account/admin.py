from django.contrib import admin
from .models import User, Landlord, Contact, UserProfile, Agent

# Register your models here.
admin.site.register(User)
admin.site.register(Landlord)
admin.site.register(Contact)
admin.site.register(UserProfile)
admin.site.register(Agent)

