from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from io import BytesIO
import base64

def handle_uploaded_file(file):
    file_path = os.path.join('media', file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            df = pd.read_csv(file_path)
            # Basic Data Analysis
            summary_stats = df.describe().to_html()
            missing_values = df.isnull().sum().reset_index()
            missing_values.columns = ['Column', 'Missing Values']
            missing_values_html = missing_values.to_html()
            # Generate plots
            plt.figure()
            fig, ax = plt.subplots()
            df.hist(ax=ax)
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            image_b64 = base64.b64encode(image_png).decode('utf-8')
            return render(request, 'analysis/results.html', {
                'df': df.head().to_html(),
                'summary_stats': df.describe().to_html(),
                'missing_values': df.isnull().sum().to_frame('Missing Values').to_html(),
                'image': image_b64,
            })
    else:
        form = UploadFileForm()
    return render(request, 'analysis/upload.html', {'form': form})

