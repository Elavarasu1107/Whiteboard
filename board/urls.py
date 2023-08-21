from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardRest.as_view({'post': 'create', 'get': 'list'}), name='board'),
    path('<int:pk>', views.BoardRest.as_view({'get': 'retrieve', 'put': 'update'}), name='board'),
    path('share/', views.CollaboratorRest.as_view({'post': 'create', 'delete': 'destroy'}), name='share'),
]
