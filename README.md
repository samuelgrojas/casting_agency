
# Casting Agency API

## Descripción del Proyecto
Esta API permite gestionar actores y películas para una agencia de casting. Incluye autenticación basada en roles (RBAC) usando Auth0, y permite realizar operaciones CRUD sobre actores y películas.

## Motivación
Este proyecto forma parte del programa Full Stack Nanodegree de Udacity. El objetivo es construir una API segura, bien documentada y desplegable que cumpla con los estándares profesionales.

## URL del Despliegue
Actualmente no desplegado. Se recomienda usar plataformas como Render (gratuita) para el despliegue.

## Autenticación con Auth0
La API requiere autenticación JWT. Se usa Auth0 con el flujo de contraseña (password grant).

### Obtener un token JWT con `curl`
```bash
curl --request POST   --url https://dev-37mr64f34epz156f.us.auth0.com/oauth/token   --header 'content-type: application/json'   --data '{
    "grant_type": "password",
    "username": "castingdirector@castingagency.com",
    "password": "Castingdirector.",
    "audience": "casting-agency",
    "client_id": "1mkQQV1DGuSwup0Snu1eVtvm5oQvxfNS",
    "client_secret": "yjjTGhHapYf2bWBgEdf-9-FgD9rdiya9gxEZdxKR1uZLuZV4VeA0nqBpbAghB0Zb",
    "connection": "Username-Password-Authentication"
  }'
```

## Instalación y Desarrollo Local
```bash
# Clonar el repositorio
https://github.com/tuusuario/casting-agency.git

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

## 📚 Endpoints y RBAC

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

## Código y Estilo
- Cumple con PEP8
- Variables y funciones con nombres claros
- Código comentado y mantenible
- Secrets gestionados con variables de entorno
