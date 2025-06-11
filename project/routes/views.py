import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from packages.models import Paquete
from .models import Sede


def geocode_address(address):
    url = (
        f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
        f"?limit=1&access_token={settings.MAPBOX_TOKEN}"
    )
    r = requests.get(url)
    data = r.json()
    if data.get('features'):
        lon, lat = data['features'][0]['center']
        return lon, lat
    return None

class CrearRutaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        destinos_ids = request.data.get('paquetes')
        if not destinos_ids:
            return Response({"error": "Paquetes son requeridos"}, status=400)

        sede = Sede.objects.first()
        if not sede:
            return Response({"error": "Sede no configurada"}, status=500)

        sede_coords = geocode_address(sede.direccion)
        if not sede_coords:
            sede_coords = [sede.longitud, sede.latitud]

        puntos = [sede_coords]

        for pid in destinos_ids:
            try:
                paquete = Paquete.objects.get(id=pid)
            except Paquete.DoesNotExist:
                return Response({"error": f"Paquete con id {pid} no existe"}, status=404)

            coords = geocode_address(paquete.direccion_destino)
            if not coords:
                coords = [paquete.longitud, paquete.latitud]
            puntos.append(coords)

        # Construir la cadena para la URL de Mapbox Optimization API
        coord_str = ';'.join([f"{lon},{lat}" for lon, lat in puntos])
        mapbox_url = (
            f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{coord_str}"
            f"?overview=full&geometries=geojson&access_token={settings.MAPBOX_TOKEN}"
        )

        try:
            response = requests.get(mapbox_url)
            data = response.json()

            if 'trips' in data:
                ruta = data['trips'][0]
                return Response({
                    "distancia_total_m": ruta['distance'],
                    "duracion_total_s": ruta['duration'],
                    "geometry": ruta['geometry']
                })
            else:
                return Response({"error": "No se pudo calcular la ruta"}, status=500)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class SedeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sede = Sede.objects.first()
        if not sede:
            return Response({"error": "Sede no configurada"}, status=404)
        return Response({
            "direccion": sede.direccion,
            "latitud": sede.latitud,
            "longitud": sede.longitud,
        })

    def post(self, request):
        if request.user.rol != 'admin':
            return Response({"error": "No autorizado"}, status=403)

        direccion = request.data.get('direccion')
        lat = request.data.get('latitud')
        lon = request.data.get('longitud')

        if not direccion or lat is None or lon is None:
            return Response({"error": "Faltan datos"}, status=400)

        sede = Sede.objects.first()
        if sede:
            sede.direccion = direccion
            sede.latitud = lat
            sede.longitud = lon
            sede.save()
        else:
            Sede.objects.create(direccion=direccion, latitud=lat, longitud=lon)

        return Response({"message": "Sede actualizada"})

