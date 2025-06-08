import requests



def get_route_JSON(base_url,origin, destination):
    """
        Calcula la ruta más rápida entre 'origin' y 'destination'.

        Parámetros:
            origin: Tuple[float, float]  # (lon, lat)
            destination: Tuple[float, float]  # (lon, lat)

        Retorna:
            Diccionario con, al menos, keys:
              - distance (float): distancia total en metros
              - duration (float): duración total en segundos
              - geometry (dict): GeoJSON de la ruta
              - steps (List[dict]): instrucciones paso a paso (opcional)
    """
    """
        origin[0]: float  # longitud del origen
        origin[1]: float  # latitud del origen
        destination[0]: float  # longitud del destino
        destination[1]: float  # latitud del destino
        Retorna un diccionario con la ruta más rápida entre 'origin' y 'destination'.
    """
    url = f"{base_url}/route/v1/driving/{origin[0]},{origin[1]};{destination[0]},{destination[1]}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_trip_JSON(base_url,waypoints):
    """
        Calcula la ruta más rápida entre múltiples puntos de paso.

        Parámetros:
            waypoints: List[Tuple[float, float]]  # Lista de tuplas (lon, lat)

        Retorna:
            Diccionario con, al menos, keys:
              - distance (float): distancia total en metros
              - duration (float): duración total en segundos
              - geometry (dict): GeoJSON de la ruta
              - steps (List[dict]): instrucciones paso a paso (opcional)
    """
    waypoints_str = ";".join([f"{wp[0]},{wp[1]}" for wp in waypoints])
    url = f"{base_url}/trip/v1/driving/{waypoints_str}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
