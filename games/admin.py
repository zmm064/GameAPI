from django.contrib import admin
from .models import GameCategory, Game
# Register your models here.

admin.site.register(Game)
admin.site.register(GameCategory)
