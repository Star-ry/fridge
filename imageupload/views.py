from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import Image
import torch
from PIL import Image as PILImage

from django.conf import settings

# def load_yolov7_model():
#     model = torch.hub.load('WongKinYiu/yolov7', 'custom', path_or_model='path/to/yolov7.pt')
#     return model

# # 모델 인스턴스 생성 (프로젝트 시작 시 한 번만 로드)
# yolov7_model = load_yolov7_model()

def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            image_path = image_instance.image.path
            processed_image_path = process_image_with_yolov7(None, image_path)
            relative_processed_image_path = os.path.relpath(processed_image_path, settings.MEDIA_ROOT)
            return render(request, 'imageupload/image_result.html', {'processed_image_path': relative_processed_image_path})
    else:
        form = ImageForm()
    return render(request, 'imageupload/image_upload.html', {'form': form})

import os
def process_image_with_yolov7(model, image_path):
    # 이미지 로드
    img = PILImage.open(image_path)
    
    # 모델 추론
    # results = model(img)
    
    # 결과 처리 (예: 바운딩 박스 그리기 등)
    # results.print()  # 터미널에 결과 출력 (디버깅용)
    processed_image_name = os.path.basename(image_path)
    # processed_image_dir = os.path.join(settings.MEDIA_ROOT, 'processed')
    processed_image_dir = os.path.join(settings.MEDIA_ROOT, 'images')
    os.makedirs(processed_image_dir, exist_ok=True)
    processed_image_path = os.path.join(processed_image_dir, processed_image_name)
    # results.save(save_dir=processed_image_dir)
    
    return processed_image_path