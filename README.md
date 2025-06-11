# SitemaLogistica

## Configuración

Para ejecutar el proyecto es necesario definir las siguientes variables de entorno:

- `SECRET_KEY`: Clave secreta de Django.
- `DATABASE_URL`: URL de conexión a la base de datos.
- `MAPBOX_TOKEN`: Token de acceso a la API de Mapbox.
  Puedes obtener uno creando una cuenta gratuita en [Mapbox](https://account.mapbox.com/).

Sin estos valores la aplicación no podrá inicializarse correctamente.

Se incluye un archivo `.env.example` con valores de ejemplo. Copia este archivo a
`.env` para utilizarlo:

```bash
cp .env.example .env
```

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

## Comandos de gestión principales

- `python project/manage.py runserver` ─ Inicia el servidor en modo desarrollo.
- `python project/manage.py makemigrations` ─ Crea archivos de migración a partir de los cambios en los modelos.
- `python project/manage.py migrate` ─ Aplica las migraciones a la base de datos.
- `python project/manage.py createsuperuser` ─ Genera un usuario administrador para acceder al panel de administración.

Con estos comandos podrás administrar y probar el sistema de logística en tu entorno local.
