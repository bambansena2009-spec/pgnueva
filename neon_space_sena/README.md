# NEON SPACE — Sistema de Información SENA

Proyecto individual desarrollado con Flask, HTML, CSS, JavaScript y SQL.

## Estructura
- `app.py`: servidor Flask, autenticación y CRUD.
- `templates/`: páginas HTML.
- `static/css/style.css`: diseño visual.
- `static/js/script.js`: interacciones.
- `sql/schema.sql`: estructura y datos iniciales PostgreSQL.
- `render.yaml`: configuración para despliegue en Render.
- `requirements.txt`: dependencias.

## Ejecutar en Visual Studio Code

### 1. Crear entorno virtual
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar
```bash
python app.py
```

Abrir:
`http://127.0.0.1:5000`

## Base de datos local
Sin `DATABASE_URL`, la aplicación usa SQLite (`neon_space.db`) para pruebas locales.

## Producción
En Render se debe configurar `DATABASE_URL` con la cadena de conexión de PostgreSQL y `SECRET_KEY` con un valor seguro.

Build Command:
```bash
pip install -r requirements.txt
```

Start Command:
```bash
gunicorn app:app
```

## Despliegue recomendado: Render
Render permite desplegar aplicaciones Flask como Web Service y proporciona un subdominio `onrender.com`. La aplicación debe usar Gunicorn en producción.

Pasos:
1. Crear cuenta en Render.
2. Subir este proyecto a GitHub.
3. En Render elegir New > Web Service.
4. Conectar el repositorio.
5. Runtime: Python.
6. Build Command: `pip install -r requirements.txt`.
7. Start Command: `gunicorn app:app`.
8. Elegir Free para una demostración académica.
9. Crear una base PostgreSQL.
10. Copiar su `Internal Database URL` como variable `DATABASE_URL`.
11. Crear `SECRET_KEY`.
12. Desplegar.
13. Probar `/`, `/registro`, `/login`, `/panel` y `/health`.

## Dominio
Render entrega un subdominio `nombre.onrender.com`. También permite asociar un dominio personalizado desde la configuración del servicio. Para un dominio propio se debe comprar/usar un dominio y crear los registros DNS que indique Render.

## Importante sobre el plan gratuito
Los servicios web gratuitos pueden suspenderse después de inactividad y PostgreSQL gratuito tiene límites. Para una evidencia académica es suficiente como entorno de demostración, pero no debe presentarse como infraestructura empresarial permanente.

## Evidencias
Tomar capturas de:
1. Proyecto abierto en Visual Studio Code.
2. Base de datos SQL.
3. Registro de usuario.
4. Inicio de sesión.
5. Panel CRUD.
6. Creación de un servicio.
7. Edición de un servicio.
8. Eliminación de un servicio.
9. URL pública funcionando.
10. Configuración de variables de entorno.
11. Base de datos PostgreSQL en el hosting.
12. Prueba desde celular o segundo dispositivo.
