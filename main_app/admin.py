from django.contrib import admin

# Register your models here.
from .models import Agent, Client, Listing

admin.site.register(Agent)
admin.site.register(Client)
admin.site.register(Listing)