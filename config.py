import os

# Cargar variables desde un archivo .env en desarrollo local (si existe).
# En produccion (Railway / Render / etc.) las variables se definen en el panel.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _as_bool(valor):
    return str(valor).lower() in ('1', 'true', 'yes', 'on')


class Config:
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'medical_app_db')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))

    # Activar SSL/TLS cuando el proveedor de BD lo exige (Aiven, TiDB, etc.).
    # En MySQL local o en la red interna de Railway debe quedar en false.
    DB_SSL = _as_bool(os.environ.get('DB_SSL', 'false'))

    # Clave para firmar los tokens JWT.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'USAT2026$$**01')
