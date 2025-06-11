# SitemaLogistica

## Configuración

Para ejecutar el proyecto es necesario definir las siguientes variables de entorno:

- `SECRET_KEY`: Clave secreta de Django.
- `DATABASE_URL`: URL de conexión a la base de datos.
- `MAPBOX_TOKEN`: Token de acceso a la API de Mapbox.

Sin estos valores la aplicación no podrá inicializarse correctamente.

Instala las dependencias y ejecuta las migraciones antes de iniciar el
servidor:

```bash
pip install -r requirements.txt
python3 project/manage.py migrate
python3 project/manage.py runserver
```

Este proyecto es una aplicación web desarrollada con Django para gestionar paquetes, rutas y usuarios de un sistema logístico. Incluye un panel de administración, vistas para conductores y clientes, y un módulo frontend con recursos estáticos.

## Puesta en marcha

Sigue los siguientes pasos para levantar el proyecto en un entorno de desarrollo:

1. **Crear y activar un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```
2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
3. **Ejecutar migraciones**
   ```bash
   python project/manage.py makemigrations
   python project/manage.py migrate
   ```
4. **Levantar el servidor de desarrollo**
   ```bash
   python project/manage.py runserver
   ```
