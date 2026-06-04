from conexionBD import Conexion

class Medico:
    def __init__(self, id=None):
        self.id = id

    def consultarMedicos(self):
        #Abrir una conexion
        con = Conexion().open

        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()

        #Definir la sentencia SQL
        sql = """
            SELECT
                m.id AS id,
                CONCAT(m.nombres, ' ', m.apellidos) AS nombre,
                COALESCE(MIN(e.nombre), 'Sin especialidad') AS especialidad,
                COALESCE(m.horario, 'Por definir') AS horario,
                COALESCE(m.consultorio, '-') AS consultorio
            FROM medico m
            LEFT JOIN medico_especialidad me ON me.medico_id = m.id
            LEFT JOIN especialidad e ON e.id = me.especialidad_id
            WHERE m.estado_medico_id = 1
            GROUP BY m.id, m.nombres, m.apellidos, m.horario, m.consultorio
            ORDER BY m.id;
        """

        cursor.execute(sql)

        #Recuperar los datos de los medicos
        resultado = cursor.fetchall()

        cursor.close()
        con.close()

        return resultado

    def obtener_medico_por_id(self, medico_id):
        """Obtiene un medico por ID"""
        con = Conexion().open
        cursor = con.cursor()

        sql = """
            SELECT
                m.id AS id,
                CONCAT(m.nombres, ' ', m.apellidos) AS nombre,
                COALESCE(MIN(e.nombre), 'Sin especialidad') AS especialidad,
                COALESCE(m.horario, 'Por definir') AS horario,
                COALESCE(m.consultorio, '-') AS consultorio
            FROM medico m
            LEFT JOIN medico_especialidad me ON me.medico_id = m.id
            LEFT JOIN especialidad e ON e.id = me.especialidad_id
            WHERE m.id = %s
            GROUP BY m.id, m.nombres, m.apellidos, m.horario, m.consultorio;
        """

        cursor.execute(sql, [medico_id])
        resultado = cursor.fetchone()

        cursor.close()
        con.close()

        return resultado

    def obtener_imagen(self, medico_id):
        #Abrir conexión
        con = Conexion().open

        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()

        #Definir la sentencia SQL
        sql = """
           select coalesce(foto, 'x') as foto from medico where id = %s
        """

        #Ejecutar la sentencia SQL
        cursor.execute(sql, [medico_id])

        #Recuperar los datos
        resultado = cursor.fetchone()

        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()

        #Verificar si se encontró la imagen
        if resultado and resultado['foto'] != 'x':
            return resultado
        else: #No se encontró la imagen
            return None
