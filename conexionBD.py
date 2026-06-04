import MySQLdb as dbc
import MySQLdb.cursors
from config import Config

class Conexion:
    def __init__(self):
        kwargs = dict(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            passwd=Config.DB_PASSWORD,
            db=Config.DB_NAME,
            port=Config.DB_PORT,
            cursorclass=dbc.cursors.DictCursor,
            # Forzar UTF-8 para que los acentos y la ñ se lean/escriban bien
            # (sin esto, "Pediatría" se ve como "PediatrÃ­a").
            charset='utf8mb4',
            use_unicode=True
        )

        # Proveedores como Aiven o TiDB exigen conexion cifrada (TLS).
        # ssl_mode='REQUIRED' cifra la conexion sin requerir el certificado CA.
        if Config.DB_SSL:
            kwargs['ssl_mode'] = 'REQUIRED'

        self.dblink = dbc.connect(**kwargs)

    @property
    def open(self):
        return self.dblink
