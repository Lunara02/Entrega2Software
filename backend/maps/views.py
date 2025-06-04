# backend/maps/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CalculaRutaAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Más adelante, aquí llamaremos a un servicio externo para calcular rutas.
        origen = request.query_params.get('origen')
        destino = request.query_params.get('destino')
        # Por ahora devolvemos un JSON de ejemplo:
        return Response({
            'origen': origen,
            'destino': destino,
            'ruta': 'POLILINEA_ENCRIPTADA_O_COORDENADAS'
        })
