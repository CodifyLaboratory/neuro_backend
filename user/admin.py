from django.contrib import admin
from .models import User, UserProfile, City, Country, Gender
from django.contrib.auth.models import Group

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(City)
admin.site.register(Country)
admin.site.unregister(Group)
admin.site.register(Gender)