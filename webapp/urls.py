# webapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_notes, name='upload_notes'),
    path('export-csv/', views.export_csv, name='export_csv'), 
     path('meetings/', views.list_meetings, name='list_meetings'),  
    path('view-meeting/<str:meeting_id>/', views.view_meeting, name='view_meeting'),  
]