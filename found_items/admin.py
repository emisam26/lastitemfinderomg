# from django.contrib import admin
# from .models import Item

# class ItemAdmin(admin.ModelAdmin):
#     item_display = ('id', 'title', 'location', 'description', 'date_found')
#     item_display_links = ('id', 'title', 'date_found')
#     item_filter = ('id',)
#     search_fields = ('title', 'description', 'location')
#     item_per_page = 20

# admin.site.register(Item, ItemAdmin)

from django.contrib import admin
from .models import Item
from .utils import upload_to_supabase
import os

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date_found')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Save to DB first

        if obj.photo:
            file_path = obj.photo.path
            supabase_path = f"photos/{os.path.basename(file_path)}"
            public_url = upload_to_supabase(file_path, supabase_path)
            if public_url and public_url != obj.supabase_url:
                obj.supabase_url = public_url
                obj.save(update_fields=['supabase_url'])
