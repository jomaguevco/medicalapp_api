# =====================================================================
#  PLANTILLA DE CONFIGURACION
#
#  1. Copia este archivo como  config.py
#  2. Reemplaza los valores segun tu entorno (local o PythonAnywhere)
#
#  config.py esta en .gitignore (NO se sube a GitHub por seguridad).
# =====================================================================

class Config:
    # -----------------------------------------------------------------
    # OPCION A) LOCAL (XAMPP / MySQL en tu PC)
    # -----------------------------------------------------------------
    # DB_HOST = '127.0.0.1'
    # DB_USER = 'root'
    # DB_PASSWORD = 'TU_PASSWORD_LOCAL'
    # DB_NAME = 'medical_app_db'
    # DB_PORT = 3306

    # -----------------------------------------------------------------
    # OPCION B) PYTHONANYWHERE
    #   - El host es:   <usuario>.mysql.pythonanywhere-services.com
    #   - El usuario es tu usuario de PythonAnywhere
    #   - El nombre de la BD lleva el prefijo:  <usuario>$medical_app_db
    #   - El password es el de la base de datos (pestaña "Databases")
    # -----------------------------------------------------------------
    DB_HOST = 'jomaguevco.mysql.pythonanywhere-services.com'
    DB_USER = 'jomaguevco'
    DB_PASSWORD = 'TU_PASSWORD_DE_BD_EN_PYTHONANYWHERE'
    DB_NAME = 'jomaguevco$medical_app_db'
    DB_PORT = 3306

    # Clave para firmar los tokens JWT (cambiala por una propia)
    SECRET_KEY = 'USAT2026$$**01'
