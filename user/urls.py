from django.urls import path
from . import views

urlpatterns = [
    path('signUp/', views.UserRest.as_view({'post': 'create'}), name='user'),
    path('signIn/', views.UserRest.as_view({'post': 'sign_in'}), name='user'),
    path('signOut/', views.UserRest.as_view({'get': 'sign_out'}), name='user'),
]
