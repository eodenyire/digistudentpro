from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ViewSet):
    
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update_streak(self, request, pk=None):
        user = self.get_object(pk)
        # Your logic to update streak
        return Response(status=status.HTTP_200_OK)

    def add_points(self, request, pk=None):
        user = self.get_object(pk)
        # Your logic to add points
        return Response(status=status.HTTP_200_OK)

    def get_object(self, pk):
        return User.objects.get(pk=pk)