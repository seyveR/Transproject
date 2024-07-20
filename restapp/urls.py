from django.urls import path
from .views import PhotoUploadView

urlpatterns = [
    path('api/photos/', PhotoUploadView.as_view(), name='photo-upload'),
]