# MedicalApp - API REST (Flask)

API REST para la aplicación móvil MedicalApp (gestión de usuarios, médicos,
especialidades y citas) con autenticación JWT y MySQL.

## Estructura

```
medicalapp_api/
├── app.py                 # Punto de entrada Flask (registra los blueprints)
├── conexionBD.py          # Conexión a MySQL (SSL opcional)
├── config.py              # Configuración por variables de entorno
├── .env.example           # Plantilla de variables de entorno (copiar a .env)
├── Procfile               # Arranque en la nube (gunicorn)
├── requirements.txt       # Dependencias
├── medical_app_db.sql     # Esquema + datos de prueba (phpMyAdmin / MySQL)
├── models/                # Lógica de acceso a datos
├── routes/                # Endpoints (blueprints)
├── tools/                 # JWT y utilidades
└── uploads/fotos/         # Imágenes (usuarios, médicos, especialidades)
```

## Instalación local

```bash
pip install -r requirements.txt
cp .env.example .env                 # y editar con tus datos de MySQL local
python app.py                        # corre en http://127.0.0.1:3007
```

Importar `medical_app_db.sql` desde phpMyAdmin para crear la base de datos
`medical_app_db` con datos de prueba.

**Usuarios de prueba** (contraseña de todos: `usat`):
- `admin@clinica.com` (administrativo)
- `ana.torres@gmail.com` (paciente)
- `maria.lopez@clinica.com`, `jose.rivera@clinica.com`, ... (médicos)

## Despliegue en la nube (Railway / Render)

La app está lista para cualquier PaaS: usa `gunicorn` (ver `Procfile`) y toma
toda su configuración de **variables de entorno** (las mismas de `.env.example`).

Pasos generales:
1. Conectar el repo de GitHub al hosting.
2. Crear/usar una base de datos MySQL y cargar `medical_app_db.sql`.
3. Definir las variables de entorno (`DB_HOST`, `DB_USER`, `DB_PASSWORD`,
   `DB_NAME`, `DB_PORT`, `DB_SSL`, `SECRET_KEY`).
   - Railway (MySQL interno): `DB_SSL=false`
   - Aiven / TiDB (MySQL externo): `DB_SSL=true`
4. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

> Nota: PythonAnywhere **gratuito** no sirve para esto: no incluye MySQL ni
> permite conexiones MySQL salientes a hosts externos.
