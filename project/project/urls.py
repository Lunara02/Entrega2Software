from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import LoginView, LogoutView, CheckAuthView, CurrentUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/check-auth/', CheckAuthView.as_view(), name='check_auth'),
    path('api/current-user/', CurrentUserView.as_view(), name='current_user'),
    path('api/users/', include('users.urls')),
    path('api/packages/', include('packages.urls')),
    path('api/routes/', include('routes.urls')),
    path('api/assignments/', include('assignments.urls')),
    path('api/admin/', include('admin_panel.urls')),
    path('', include('frontend.urls')),
    
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
