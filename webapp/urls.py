# webapp/urls.py

from django.urls import path

from webapp import api_views
from . import views

urlpatterns = [
    path('', views.upload_notes, name='upload_notes'),
    path('export-csv/', views.export_csv, name='export_csv'), 
     path('meetings/', views.list_meetings, name='list_meetings'),  
    path('view-meeting/<str:meeting_id>/', views.view_meeting, name='view_meeting'),  

     path('api/pending/', api_views.get_pending_actions, name='api_pending'),
    path('api/meetings/', api_views.get_all_meetings, name='api_meetings'),
    
]