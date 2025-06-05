from django.db import models
from datetime import datetime
import os
from supabase import create_client
 
# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
 
MEDIA_URL = f"{SUPABASE_URL}/storage/v1/object/public/media/"
 
class UploadedFile(models.Model):
    image = models.ImageField(upload_to="uploads/")
 
    def save(self, *args, **kwargs):
        if not self.image:
            super().save(*args, **kwargs)
            return
 
        file_name = self.image.name  # Example: "myphoto.jpg"
        subfolder_path = f"photos/{file_name}"  # Now it goes into 'media/photos/'
 
        file_data = self.image.file  # File data
 
        print(f"Uploading {file_name} to Supabase in 'photos/' subfolder...")
 
        # Upload to Supabase inside the "photos/" folder
        response = supabase.storage.from_("media").upload(subfolder_path, file_data)
 
        if "error" in response:
            print(f"Upload failed: {response['error']}")
        else:
            print(f"File uploaded successfully: {MEDIA_URL}{subfolder_path}")
            self.image = f"{MEDIA_URL}{subfolder_path}"  # Store URL in database
 
        super().save(*args, **kwargs)
         
         
class Item(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    date_found = models.DateTimeField(default=datetime.now, blank=True)
    
def __str__(self):
    return self.title