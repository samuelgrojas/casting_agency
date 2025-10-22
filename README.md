
# Casting Agency API

## Descripción del Proyecto
Esta API permite gestionar actores y películas para una agencia de casting. Incluye autenticación basada en roles (RBAC) usando Auth0, y permite realizar operaciones CRUD sobre actores y películas.

## Motivación
Este proyecto forma parte del programa Full Stack Nanodegree de Udacity. El objetivo es construir una API segura, bien documentada y desplegable que cumpla con los estándares profesionales.

## URL del Despliegue
El proceso está desplegado en Render y se puede acceder a través del siguiente link: https://render-deployment-example-pok5.onrender.com/

## Autenticación con Auth0
La API requiere autenticación JWT. Se usa Auth0 con el flujo de contraseña (password grant).

### Obtener un token JWT con `curl` (Ejemplo)

curl --request POST \
  --url https://dev-37mr64f34epz156f.us.auth0.com/oauth/token \
  --header 'content-type: application/json' \
  --data '{
    "grant_type": "password",
    "username": "castingdirector@castingagency.com",
    "password": "Castingdirector.",
    "audience": "casting-agency",
    "client_id": "1mkQQV1DGuSwup0Snu1eVtvm5oQvxfNS",
    "connection": "Username-Password-Authentication"
  }'

### Llamar a un endpoint protegido con el access_token devuelto

curl --request GET \
  --url https://render-deployment-example-pok5.onrender.com/actors \
  --header "Authorization: Bearer YOUR_ACCESS_TOKEN"

## Roles y Permisos en Auth0
La API utiliza RBAC (Role-Based Access Control). Los roles están configurados en Auth0 y asignan permisos específicos a cada usuario. Por ejemplo:

Casting Assistant: get:actors, get:movies
Casting Director: get, post, patch, delete sobre actores
Executive Producer: todos los permisos

Los permisos se configuran en Auth0 en la sección de APIs → Permissions, y se asignan a roles en User Management → Roles.

## Seguridad y Tokens de Prueba
Por razones de seguridad, el client_secret no se incluye en este README. Si necesitas un token de prueba para revisar la API, puedes:

Solicitarlo directamente al autor del proyecto
Usar un token de corta duración proporcionado por el autor

## Instalación y Desarrollo Local
```bash
# Clonar el repositorio
https://github.com/samuelgrojas/casting_agency.git

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Ejecutar Tests
```bash
python test_app.py
```

## Endpoints y RBAC

### GET /actors
- Requiere permiso: `get:actors`
- Devuelve lista de actores

### GET /movies
- Requiere permiso: `get:movies`
- Devuelve lista de películas

### POST /actors
- Requiere permiso: `post:actors`
- Crea un nuevo actor

### POST /movies
- Requiere permiso: `post:movies`
- Crea una nueva película

### PATCH /actors/<id>
- Requiere permiso: `patch:actors`
- Actualiza un actor existente

### PATCH /movies/<id>
- Requiere permiso: `patch:movies`
- Actualiza una película existente

### DELETE /actors/<id>
- Requiere permiso: `delete:actors`
- Elimina un actor

### DELETE /movies/<id>
- Requiere permiso: `delete:movies`
- Elimina una película


## Ejecutar Tests con Autenticación
Para ejecutar los tests correctamente, necesitas definir un token JWT válido en una variable de entorno llamada TEST_TOKEN. Puedes hacerlo de la siguiente manera:
```
export TEST_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."  # Reemplaza con tu token real
python test_app.py
```

También puedes usar un archivo .env con la siguiente estructura:
```
TEST_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```
Y cargarlo automáticamente con python-dotenv.

## Despliegue en Render
La aplicación está desplegada en https://render.com. Para desplegarla correctamente, asegúrate de configurar las siguientes variables de entorno en el panel de configuración del servicio:

- AUTH0_DOMAIN
- API_AUDIENCE
- AUTH0_CLIENT_ID
- FLASK_APP=app.py
- FLASK_ENV=production
- DATABASE_URL (si usas PostgreSQL en Render)

Pasos básicos para desplegar:

1. Crear un nuevo servicio web en Render.
2. Conectar el repositorio de GitHub.
3. Configurar las variables de entorno.
4. Render instalará automáticamente las dependencias desde requirements.txt.
5. La app se iniciará con el comando gunicorn app:app.

## Dependencias Principales
Las dependencias están listadas en requirements.txt, pero las más relevantes son:

- Flask – Framework principal para la API
- SQLAlchemy – ORM para la base de datos
- Flask-Migrate – Migraciones de base de datos
- python-dotenv – Carga de variables de entorno desde .env
- Authlib – Validación de tokens JWT
- unittest – Framework de testing