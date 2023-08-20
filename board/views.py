from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Q
from user.utils import SessionAuth
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.exceptions import exception_handler, ApiException
from .serializers import BoardSerializer, CollaboratorSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Board, BoardDetails


# Create your views here.
class BoardRest(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(Q(user_id=self.request.user.id) | Q(collaborators__id=self.request.user.id))

    @exception_handler
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Board Created', 'status': 201, 'data': {}})

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({'message': 'All boards Retrieved', 'status': 200, 'data': response.data})

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        board_details = BoardDetails.objects.filter(board_id=response.data['id'], user_id=response.data['user']).values()
        return Response({'message': 'Board Retrieved', 'status': 200, 'data': [response.data, board_details]})


class CollaboratorRest(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CollaboratorSerializer

    @exception_handler
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        board = Board.objects.filter(id=request.data.get('id'), user_id=request.user.id).first()
        if not board:
            raise ApiException(message='Board not found or access denied', status=406)
        board.collaborators.add(*request.data.get('collaborators'))
        board.save()
        return Response({'message': 'Board shared successfully', 'status': 200}, status=200)

    def destroy(self, request, *args, **kwargs):
        board = Board.objects.get(id=request.data.get('id'), user_id=request.user.id).first()
        if not board:
            raise ApiException(message='Board not found', status=404)
        board.collaborators.remove(*request.data.get('collaborators'))
        board.save()
        return Response({'message': 'Board removed', 'status': 200}, status=200)


class EditorView(View):

    def get(self, request, board_id):
        if request.user.is_authenticated:
            board = Board.objects.filter(id=board_id, user_id=request.user.id).first()
            collaborators = []
            if board:
                collaborators = list(board.collaborators.all().values_list('id', flat=True))
            return render(request, 'board/editor.html', context={'board': board, 'collaborators': collaborators})
        return redirect('login_page')
