from django.urls import path
from .views import RegisterUserView
from users.views import LoginView, LogoutView, CheckAuthView, CurrentUserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check-auth/', CheckAuthView.as_view(), name='check_auth'),
    path('current-user/', CurrentUserView.as_view(), name='current_user'),
]

