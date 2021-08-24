from django.contrib import admin

# Register your models here.
from .models import Measurement,Profile

admin.site.register(Measurement)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(Profile, ProfileAdmin)
