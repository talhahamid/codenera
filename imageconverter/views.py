from django.shortcuts import render, redirect
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from imageconverter.models import ImagesStore
from accounts.models import Users
import os
from django.core.files.base import ContentFile
from django.conf import settings




def add_watermark(image, text="Codenera", font_size=14):
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    position = (width - text_width - 20, height - text_height - 20)
    padding = 10    
    rect_position = [
        position[0] - padding, 
        position[1] - padding, 
        position[0] + text_width + padding, 
        position[1] + text_height + padding
    ]
    draw.rectangle(rect_position, fill=(0, 255, 255, 128))  
    draw.text(position, text, fill=(0, 0, 0), font=font)
    return image




def convertimg(request):
    converted_image_data = None  
    if request.method == "POST":
        image_file = request.FILES['image'] 
        size = request.POST['size']
        watermark = request.POST['watermark']

        image = Image.open(image_file)

        sizes = {
            'thumbnail': (100, 100),
            'medium': (500, 500),
            'large': (1000, 1000),
        }

        resize_and_watermark = lambda img, s: add_watermark(img.resize(s, Image.Resampling.LANCZOS), text=watermark)

        if size in sizes:
            resized_image = resize_and_watermark(image, sizes[size])
            img_byte_arr = io.BytesIO()
            resized_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            if request.session.get('id'):
                user = Users.objects.get(id=request.session.get('id'))
                image_file_name = f"user_{user.id}_image.png"
                
                media_path = os.path.join(settings.MEDIA_ROOT)
                
                if not os.path.exists(media_path):
                    os.makedirs(media_path)
                
                file_path = os.path.join(media_path, image_file_name)
                
                with open(file_path, 'wb') as f:
                    f.write(img_byte_arr.getvalue())
                
                ImagesStore.objects.create(user=user, image=image_file_name)

                converted_image_data = ContentFile(img_byte_arr.getvalue(), name=f"converted_{image_file.name}")

                base64_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            

        return render(request, 'home.html', {'converted_image': base64_image})

    return render(request, 'home.html')




def home(request):
    return render(request,'home.html')
