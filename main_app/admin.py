from django.contrib import admin
from .models import Agent, Client, Listing

# Register your models here.

admin.site.register(Agent)
admin.site.register(Client)
admin.site.register(Listing)