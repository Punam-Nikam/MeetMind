# webapp/api_views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from database import MongoDBHandler
from .serializers import MeetingSerializer, ActionItemSerializer

@api_view(['GET'])
def get_pending_actions(request):
    """
    API endpoint to get all pending action items.
    Slack can call this to fetch tasks.
    """
    db_handler = MongoDBHandler()
    
    if not db_handler.connect():
        return Response(
            {"error": "Could not connect to database"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    pending = db_handler.get_pending_actions()
    db_handler.close()
    
    # Serialize the data
    serializer = ActionItemSerializer(pending, many=True)
    return Response({
        "count": len(pending),
        "pending_items": serializer.data
    })

@api_view(['GET'])
def get_all_meetings(request):
    """
    API endpoint to get all meetings with their action items.
    """
    db_handler = MongoDBHandler()
    
    if not db_handler.connect():
        return Response(
            {"error": "Could not connect to database"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    meetings = db_handler.get_all_meetings()
    db_handler.close()
    
    # Serialize the data
    serializer = MeetingSerializer(meetings, many=True)
    return Response({
        "count": len(meetings),
        "meetings": serializer.data
    })