# MedicalApp - API REST (Flask)

API REST para la aplicación móvil MedicalApp (gestión de usuarios, médicos,
especialidades y citas) con autenticación JWT y MySQL.

## Estructura

```
medicalapp_api/
├── app.py                 # Punto de entrada Flask (registra los blueprints)
├── conexionBD.py          # Conexión a MySQL
├── config.example.py      # Plantilla de configuración (copiar a config.py)
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
cp config.example.py config.py      # y editar con tus datos de MySQL local
python app.py                       # corre en http://127.0.0.1:3007
```

Importar `medical_app_db.sql` desde phpMyAdmin para crear la base de datos
`medical_app_db` con datos de prueba.

**Usuarios de prueba** (contraseña de todos: `usat`):
- `admin@clinica.com` (administrativo)
- `ana.torres@gmail.com` (paciente)
- `maria.lopez@clinica.com`, `jose.rivera@clinica.com`, ... (médicos)

## Despliegue en PythonAnywhere

1. `git clone https://github.com/jomaguevco/medicalapp_api.git`
2. Crear la base de datos `<usuario>$medical_app_db` en la pestaña **Databases**.
3. Importar `medical_app_db.sql` (quitando las líneas `CREATE DATABASE` / `USE`).
4. `cp config.example.py config.py` y configurar la sección **PythonAnywhere**.
5. Crear la Web app (Flask manual), virtualenv con `requirements.txt` y apuntar
   el WSGI a `app.py` (variable `application = app`).

La API quedará disponible en `https://<usuario>.pythonanywhere.com/api/`.
