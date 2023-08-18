from django.shortcuts import render
from user.utils import SessionAuth
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.exceptions import exception_handler
from .serializers import BoardSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Board


# Create your views here.
class BoardRest(ModelViewSet):
    authentication_classes = (JWTAuthentication, SessionAuth)
    permission_classes = (IsAuthenticated,)
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user_id=self.request.user.id)

    @exception_handler
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response({'message': 'Board Created', 'status': 201, 'data': serializer.data})

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'message': 'Boards Retrieved', 'status': 200, 'data': response.data})

    def retrieve(self, request,  *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({'message': 'Board Retrieved', 'status': 200, 'data': response.data})
