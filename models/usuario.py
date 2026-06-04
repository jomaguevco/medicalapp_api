from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class Usuario:
    def __init__(self):
        self.ph = PasswordHasher()
        
    def login(self, email, clave):
        #Abrir conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = """
           SELECT 
                u.id AS usuario_id,
                u.email,
                r.nombre AS rol,
                eu.nombre AS estado_usuario,
                CONCAT( COALESCE(p.nombres, m.nombres, a.nombres), ' ', COALESCE(p.apellidos, m.apellidos, a.apellidos) ) AS nombre,
                u.password
            FROM usuario u
            INNER JOIN rol r 
                ON u.rol_id = r.id
            INNER JOIN estado_usuario eu 
                ON u.estado_usuario_id = eu.id
            LEFT JOIN paciente p 
                ON u.id = p.usuario_id
            LEFT JOIN medico m 
                ON u.id = m.usuario_id
            LEFT JOIN administrativo a 
                ON u.id = a.usuario_id
            WHERE u.email = %s
        """
        
        #Ejecutar la sentencia SQL
        cursor.execute(sql, [email])
        
        #Recuperar los datos del usuario
        resultado = cursor.fetchone()
        
        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()
        
        #Verificar si se encontró el usuario con el email ingresado
        if resultado:
            try:
                #Validar la clave almacenada en la BD con la que ingresa el usuario
                self.ph.verify(resultado['password'], clave)
                return resultado
            except VerifyMismatchError:
                return None
            
        else: #No se encontró ningún registro con el email ingresado
            return None
            
    def obtener_foto(self, usuario_id):
        #Abrir conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = """
           select coalesce(foto, 'x') as foto from usuario where id = %s
        """
        
        #Ejecutar la sentencia SQL
        cursor.execute(sql, [usuario_id])
        
        #Recuperar los datos del usuario
        resultado = cursor.fetchone()
        
        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()
        
        #Verificar si se encontró la foto del usuario
        if resultado and resultado['foto'] != 'x':
            return resultado
        else: #No se encontró la foto
            return None


    def obtener_perfil(self, usuario_id):
        con = Conexion().open
        cursor = con.cursor()
        
        sql = """
            SELECT 
                u.id AS usuario_id,
                u.email,
                r.nombre AS rol,
                COALESCE(p.nombres, m.nombres, a.nombres) AS nombres,
                COALESCE(p.apellidos, m.apellidos, a.apellidos) AS apellidos
            FROM usuario u
            INNER JOIN rol r ON u.rol_id = r.id
            LEFT JOIN paciente p ON u.id = p.usuario_id
            LEFT JOIN medico m ON u.id = m.usuario_id
            LEFT JOIN administrativo a ON u.id = a.usuario_id
            WHERE u.id = %s
        """
        
        cursor.execute(sql, [usuario_id])
        resultado = cursor.fetchone()
        
        cursor.close()
        con.close()
        
        return resultado