from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from utils.exceptions import exception_handler
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from board.models import Board


# Create your views here.
class UserRest(viewsets.ViewSet):

    @exception_handler
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'User registered', 'status': 201, 'data': serializer.data},
                        status=status.HTTP_201_CREATED)

    def list(self, request):
        board = Board.objects.get(id=request.query_params.get('id'))
        users = User.objects.all().exclude(id=board.user.id)
        serializer = RegisterSerializer(users, many=True)
        return Response({'message': 'Users retrieved', 'status': 200, 'data': serializer.data},
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def sign_in(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        login(request, serializer.instance)
        token = RefreshToken.for_user(serializer.instance)
        return Response({'message': 'Logged in successfully', 'status': 200,
                         'data': {'access': str(token.access_token), 'refresh': str(token)}},
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def sign_out(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully', 'status': 200, 'data': {}},
                        status=status.HTTP_200_OK)
