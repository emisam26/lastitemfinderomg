import os
from supabase import create_client

def upload_to_supabase(file_path, supabase_path):
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    with open(file_path, "rb") as f:
        data = f.read()

    response = supabase.storage.from_("media").upload(
        supabase_path,
        data,
        file_options={"content-type": "image/jpeg"}  # or dynamically detect content type
    )
    if response.get("error"):
        print("Upload error:", response["error"])
        return None
    else:
        return f"{SUPABASE_URL}/storage/v1/object/public/media/{supabase_path}"
