from conexionBD import Conexion


class HorarioDisponible:
    def __init__(self, id=None):
        self.id = id

    def consultar_disponibles(self, especialidad_id, desde=None, hasta=None):
        """
        Devuelve los horarios disponibles de los medicos para una especialidad.

        - especialidad_id: obligatorio.
        - desde / hasta: opcionales (formato 'YYYY-MM-DD'). Si ambos vienen,
          se filtra por el rango de fechas; si no, se devuelven todas las fechas.

        La especialidad no esta en la tabla horario_disponible, por eso se
        relaciona a traves de medico_especialidad. Las fechas y horas se
        formatean como texto para que se serialicen correctamente en el JSON.
        """
        con = Conexion().open
        cursor = con.cursor()

        sql = """
            SELECT
                hd.id AS horario_disponible_id,
                DATE_FORMAT(hd.fecha, '%%d/%%m/%%Y') AS fecha,
                TIME_FORMAT(hd.hora_inicio, '%%H:%%i') AS hora_inicio,
                TIME_FORMAT(hd.hora_fin, '%%H:%%i') AS hora_fin,

                m.id AS medico_id,
                CONCAT(m.nombres, ' ', m.apellidos) AS medico,
                m.cmp,
                m.consultorio,

                e.id AS especialidad_id,
                e.nombre AS especialidad,

                ehd.nombre AS estado_horario
            FROM horario_disponible hd
            INNER JOIN medico m
                ON hd.medico_id = m.id
            INNER JOIN medico_especialidad me
                ON me.medico_id = m.id
            INNER JOIN especialidad e
                ON me.especialidad_id = e.id
            INNER JOIN estado_horario_disponible ehd
                ON hd.estado_horario_disponible_id = ehd.id
            INNER JOIN estado_medico em
                ON m.estado_medico_id = em.id
            WHERE me.especialidad_id = %s
              AND LOWER(ehd.nombre) = 'disponible'
              AND LOWER(em.nombre) = 'activo'
              -- No mostrar horarios cuya fecha/hora ya paso respecto al momento actual.
              -- TIMESTAMP(fecha, hora_inicio) combina fecha + hora y se compara con NOW().
              AND TIMESTAMP(hd.fecha, hd.hora_inicio) > NOW()
        """

        params = [especialidad_id]

        # Filtro por rango de fechas (solo si vienen ambas)
        if desde and hasta:
            sql += " AND hd.fecha BETWEEN %s AND %s"
            params.append(desde)
            params.append(hasta)
        elif desde:
            sql += " AND hd.fecha >= %s"
            params.append(desde)
        elif hasta:
            sql += " AND hd.fecha <= %s"
            params.append(hasta)

        sql += " ORDER BY hd.fecha, hd.hora_inicio, medico;"

        cursor.execute(sql, params)
        resultado = cursor.fetchall()

        cursor.close()
        con.close()

        return resultado
