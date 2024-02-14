from django.contrib import admin
from django.urls import include, path
import buddy.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('buddy/', include('buddy.urls')),
    path('', buddy.views.Index.as_view()),    
]
