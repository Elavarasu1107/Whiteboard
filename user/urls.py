from django.urls import path
from . import views

urlpatterns = [
    path('signUp/', views.UserRest.as_view({'post': 'create', 'get': 'list'}), name='user'),
    path('signIn/', views.UserRest.as_view({'post': 'sign_in'}), name='sign_in'),
    path('signOut/', views.UserRest.as_view({'get': 'sign_out'}), name='sign_out'),
]
