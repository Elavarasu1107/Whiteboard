from django.urls import path
from . import views

urlpatterns = [
    path('api/signUp/', views.UserRest.as_view({'post': 'create'}), name='user'),
    path('api/signIn/', views.UserRest.as_view({'post': 'sign_in'}), name='user'),
    path('api/signOut/', views.UserRest.as_view({'get': 'sign_out'}), name='user'),
]
