from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Usuario y contraseña requeridos"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({
                    "message": "Login exitoso",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "rol": user.rol
                    }
                })
            else:
                return Response({"error": "Cuenta inactiva"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Sesión cerrada correctamente"})

class CheckAuthView(APIView):
    def get(self, request):
        return Response({"authenticated": request.user.is_authenticated})

class CurrentUserView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "rol": request.user.rol
            })
        return Response({"error": "No autenticado"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        rol = request.data.get('rol', 'cliente')  # por defecto es cliente

        if not username or not password:
            return Response({"error": "Faltan datos"}, status=400)

        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Usuario ya existe"}, status=400)

        user = CustomUser.objects.create_user(username=username, email=email, password=password, rol=rol)

        return Response({
            "message": "Usuario creado",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "rol": user.rol
            }
        }, status=201)
