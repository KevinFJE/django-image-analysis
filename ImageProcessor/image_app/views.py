# views.py

import os
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from .forms import ImageUploadForm
from .utils import remove_background, apply_color_filters

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_path = default_storage.save(os.path.join('original', image.name), image)
            image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
            
            # Eliminar fondo
            output_image_path = remove_background(image_full_path)
            
            # Aplicar filtros de colores
            filters_results = apply_color_filters(output_image_path)
            
            # Generar URLs para las imágenes filtradas
            filtered_image_urls = {
                'green': os.path.join(settings.MEDIA_URL, 'processed', 'filtered', 'green_filtered.png'),
                'white': os.path.join(settings.MEDIA_URL, 'processed', 'filtered', 'white_filtered.png'),
                'yellow': os.path.join(settings.MEDIA_URL, 'processed', 'filtered', 'yellow_filtered.png'),
            }

            return render(request, 'image_app/results.html', {
                'original_image_url': os.path.join(settings.MEDIA_URL, image_path),
                'filtered_image_urls': filtered_image_urls,
                'diagnosis': filters_results['diagnosis'],
                'percentages': filters_results['percentages'],
            })
    else:
        form = ImageUploadForm()
    return render(request, 'image_app/upload.html', {'form': form})
