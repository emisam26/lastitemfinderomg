# from django.db import models
# from datetime import datetime
# import os
# from supabase import create_client
# from django.conf import settings
 
# # # Load environment variables
# # SUPABASE_URL = os.getenv("SUPABASE_URL")
# # SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# # supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# # MEDIA_URL = f"{SUPABASE_URL}/storage/v1/object/public/media/"

 
# class UploadedFile(models.Model):
#     image = models.ImageField(upload_to="uploads/")

#     def save(self, *args, **kwargs):
#         if not self.image:
#             super().save(*args, **kwargs)
#             return

#         supabase_url = os.getenv("SUPABASE_URL")
#         supabase_key = os.getenv("SUPABASE_KEY")

#         if not (supabase_url and supabase_key):
#             print("🚫 Supabase credentials missing.")
#             super().save(*args, **kwargs)
#             return

#         supabase = create_client(supabase_url, supabase_key)

#         file_name = self.image.name
#         subfolder_path = f"photos/{file_name}"

#         # ✅ read the file as bytes
#         file_data = self.image.read()

#         # Try uploading
#         response = supabase.storage.from_("media").upload(
#             path=subfolder_path,
#             file=file_data,
#             file_options={"content-type": self.image.file.content_type}
#         )

#         print("📤 Upload response:", response)

#         if "error" in response and response["error"] is not None:
#             print("❌ Upload error:", response["error"])
#         else:
#             public_url = f"{supabase_url}/storage/v1/object/public/media/{subfolder_path}"
#             print(f"✅ Uploaded to: {public_url}")
#             self.image = public_url  # Save URL instead of actual file path

#         super().save(*args, **kwargs)
         
# class Item(models.Model):
#     title = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     description = models.CharField(max_length=200)
#     photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
#     date_found = models.DateTimeField(default=datetime.now, blank=True)
    
# def __str__(self):
#     return self.title

import os
from datetime import datetime
from django.db import models
from django.core.files.storage import default_storage
from supabase import create_client


class Item(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    date_found = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        # Save locally first
        super().save(*args, **kwargs)

        # Setup Supabase client
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        if not (supabase_url and supabase_key):
            print("🚫 Supabase credentials are missing.")
            return

        supabase = create_client(supabase_url, supabase_key)

        try:
            # Absolute path to file on local disk
            local_path = os.path.join(default_storage.location, self.photo.name)

            with open(local_path, "rb") as f:
                supabase_path = f"photos/{os.path.basename(self.photo.name)}"
                response = supabase.storage.from_("media").upload(
                    supabase_path, f,
                    file_options={"content-type": self.photo.file.content_type}
                )

            if response.get("error"):
                print(f"❌ Upload error: {response['error']}")
            else:
                public_url = f"{supabase_url}/storage/v1/object/public/media/{supabase_path}"
                print(f"✅ Uploaded to Supabase: {public_url}")
                self.photo.name = public_url
                super().save(update_fields=["photo"])

        except Exception as e:
            print(f"❌ Exception while uploading: {e}")

    def __str__(self):
        return self.title
