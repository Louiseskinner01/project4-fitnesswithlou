import os
import django

if os.path.isfile('env.py'):
    import env

print(f"CLOUDINARY_URL: {os.environ.get('CLOUDINARY_URL', 'NOT FOUND')}")  # ✅ debug line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fwl.settings')
django.setup()

import cloudinary.uploader

media_root = 'media/products/'

for filename in os.listdir(media_root):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
        filepath = os.path.join(media_root, filename)
        result = cloudinary.uploader.upload(filepath, public_id=f'products/{filename}')
        print(f'Uploaded: {filename} -> {result["url"]}')