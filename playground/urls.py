# urls.py

from django.urls import path
from .views import mood_detection_form, get_recommendations_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', mood_detection_form, name='mood_detection_form'),  # Empty path for default page
    
    path('get_recommendations/', get_recommendations_view, name='get_recommendations'),
    
    # Add more paths as needed
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)