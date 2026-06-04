from conexionBD import Conexion

class Especialidad:
    def __init__(self,id=None,nombre=None,descripcion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        
    def consultarEspecialidades(self):
        #Abrir una conexion
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = "SELECT id, nombre, descripcion FROM especialidad;"
        
        cursor.execute(sql)
        
        #Recuperar datos del usuario
        resultado = cursor.fetchall()
        
        cursor.close()
        con.close()
        
        return resultado
    
    def obtener_especialidad_por_id(self, especialidad_id):
        """Obtiene una especialidad por ID"""
        con = Conexion().open
        cursor = con.cursor()
        
        sql = "SELECT id, nombre, descripcion FROM especialidad WHERE id = %s"
        
        cursor.execute(sql, [especialidad_id])
        resultado = cursor.fetchone()
        
        cursor.close()
        con.close()
        
        return resultado
    
    def registrarEspecialidad(self):
        #Abrir una conexion
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = "INSERT INTO especialidad (nombre, descripcion) VALUES (%s, %s);"
        
        cursor.execute(sql,(self.nombre,self.descripcion))
        
        con.commit()
        
        cursor.close()
        con.close()
        
    def actualizarEspecialidad(self):
        #Abrir una conexion
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = "UPDATE especialidad SET nombre=%s, descripcion=%s WHERE id=%s;"
        
        cursor.execute(sql,(self.nombre,self.descripcion,self.id))
        
        con.commit()
        
        cursor.close()
        con.close()
        
    def eliminarEspecialidad(self):
        #Abrir una conexion
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = "DELETE FROM especialidad WHERE id=%s;"
        
        cursor.execute(sql,(self.id,))
        
        con.commit()
        
        cursor.close()
        con.close()

    def obtener_imagen(self, especialidad_id):
        #Abrir conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = """
           select coalesce(imagen, 'x') as imagen from especialidad where id = %s
        """
        
        #Ejecutar la sentencia SQL
        cursor.execute(sql, [especialidad_id])
        
        #Recuperar los datos
        resultado = cursor.fetchone()
        
        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()
        
        #Verificar si se encontró la imagen
        if resultado and resultado['imagen'] != 'x':
            return resultado
        else: #No se encontró la imagen
            return None
    