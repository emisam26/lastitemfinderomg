from django.db import models
from datetime import datetime
import os
from supabase import create_client
from django.conf import settings
 
# # Load environment variables
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# MEDIA_URL = f"{SUPABASE_URL}/storage/v1/object/public/media/"

 
class UploadedFile(models.Model):
    image = models.ImageField(upload_to="uploads/")

    def save(self, *args, **kwargs):
        if not self.image:
            super().save(*args, **kwargs)
            return

        from django.conf import settings

        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        if not (supabase_url and supabase_key):
            print("Supabase credentials missing")
            return

        supabase = create_client(supabase_url, supabase_key)

        file_name = self.image.name
        subfolder_path = f"photos/{file_name}"
        file_data = self.image.file

        response = supabase.storage.from_("media").upload(subfolder_path, file_data)
        if "error" in response:
            print("Upload error:", response["error"])
        else:
            self.image = f"{supabase_url}/storage/v1/object/public/media/{subfolder_path}"

        super().save(*args, **kwargs)
         
         
class Item(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    date_found = models.DateTimeField(default=datetime.now, blank=True)
    
def __str__(self):
    return self.title