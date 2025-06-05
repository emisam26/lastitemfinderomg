from django.contrib import admin
from .models import Item

class ItemAdmin(admin.ModelAdmin):
    item_display = ('id', 'title', 'location', 'description', 'date_found')
    item_display_links = ('id', 'title')
    item_filter = ('location',)
    item_per_page = 20

admin.site.register(Item, ItemAdmin)