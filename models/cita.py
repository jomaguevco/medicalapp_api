from conexionBD import Conexion

class Cita:
    def paciente_id_de_usuario(self, usuario_id):
        """Devuelve el id de paciente asociado a un usuario, o None si no existe."""
        con = Conexion().open
        cursor = con.cursor()
        try:
            cursor.execute(
                "SELECT id FROM paciente WHERE usuario_id = %s",
                [usuario_id]
            )
            fila = cursor.fetchone()
            return fila["id"] if fila else None
        finally:
            cursor.close()
            con.close()

    def listar_por_paciente(self, paciente_id):
        """
        Lista las citas de un paciente con todos los datos necesarios para
        mostrarlas en la app (fecha/hora del horario, médico, especialidad,
        consultorio y estado de la cita). Ordenadas de la más reciente a la
        más antigua según la fecha del horario.

        La especialidad se obtiene con una subconsulta sobre medico_especialidad
        para garantizar una sola fila por cita aunque el médico tuviera más de
        una especialidad. Las fechas/horas se formatean como texto para que se
        serialicen correctamente en el JSON.
        """
        con = Conexion().open
        cursor = con.cursor()
        try:
            sql = """
                SELECT
                    c.id AS cita_id,
                    c.motivo,
                    c.paciente_oncologico,
                    DATE_FORMAT(c.fecha_registro, '%%d/%%m/%%Y %%H:%%i') AS fecha_registro,

                    ec.id AS estado_cita_id,
                    ec.nombre AS estado_cita,

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

                    p.id AS paciente_id,
                    CONCAT(p.nombres, ' ', p.apellidos) AS paciente,
                    p.dni
                FROM cita c
                INNER JOIN paciente p
                    ON c.paciente_id = p.id
                INNER JOIN estado_cita ec
                    ON c.estado_cita_id = ec.id
                INNER JOIN horario_disponible hd
                    ON c.horario_disponible_id = hd.id
                INNER JOIN medico m
                    ON hd.medico_id = m.id
                LEFT JOIN especialidad e
                    ON e.id = (
                        SELECT me.especialidad_id
                        FROM medico_especialidad me
                        WHERE me.medico_id = m.id
                        LIMIT 1
                    )
                WHERE c.paciente_id = %s
                ORDER BY hd.fecha DESC, hd.hora_inicio DESC, c.id DESC
            """
            cursor.execute(sql, [paciente_id])
            return cursor.fetchall()
        finally:
            cursor.close()
            con.close()

    def registrar(self, paciente_id, paciente_oncologico, creado_por_usuario_id, citas):
        # Abrir conexión
        con = Conexion().open
        cursor = con.cursor()

        try:
            # ============================
            # 1. Validar existencia de paciente
            # ============================
            sql_validar_paciente = """
                SELECT id
                FROM paciente
                WHERE id = %s
            """
            cursor.execute(sql_validar_paciente, [paciente_id])
            paciente = cursor.fetchone()

            if not paciente:
                return False, 'El paciente no existe'

            # ============================
            # 2. Validar que exista usuario creador
            # ============================
            if not creado_por_usuario_id:
                return False, 'No se pudo identificar el usuario autenticado'

            # ============================
            # 3. Validar todos los horarios antes de registrar
            # estado_horario_disponible_id = 1 -> DISPONIBLE
            # estado_cita_id = 1 -> PENDIENTE
            # ============================
            sql_validar_horario = """
                SELECT id, estado_horario_disponible_id
                FROM horario_disponible
                WHERE id = %s
            """

            for item in citas:
                horario_disponible_id = item.get("horario_disponible_id")

                if not horario_disponible_id:
                    return False, 'Uno o más registros de cita no tienen horario_disponible_id'

                cursor.execute(sql_validar_horario, [horario_disponible_id])
                horario = cursor.fetchone()

                if not horario:
                    return False, f'El horario disponible con id {horario_disponible_id} no existe'

                if horario["estado_horario_disponible_id"] != 1:
                    return False, f'El horario con id {horario_disponible_id} ya no está disponible'

            # ============================
            # 4. Registrar citas
            # ============================
            sql_insert_cita = """
                INSERT INTO cita (
                    paciente_id,
                    horario_disponible_id,
                    motivo,
                    paciente_oncologico,
                    estado_cita_id,
                    creado_por_usuario_id
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            sql_actualizar_horario = """
                UPDATE horario_disponible
                SET estado_horario_disponible_id = 2
                WHERE id = %s
            """

            citas_registradas = []

            for item in citas:
                horario_disponible_id = item.get("horario_disponible_id")
                motivo = item.get("motivo", "")

                # Insertar cita
                cursor.execute(sql_insert_cita, [
                    paciente_id,
                    horario_disponible_id,
                    motivo,
                    paciente_oncologico,
                    1,  # estado_cita_id = 1 -> PENDIENTE
                    creado_por_usuario_id
                ])

                cita_id = cursor.lastrowid

                # Actualizar horario a RESERVADO
                cursor.execute(sql_actualizar_horario, [horario_disponible_id])

                citas_registradas.append({
                    "cita_id": cita_id,
                    "horario_disponible_id": horario_disponible_id,
                    "estado_cita": "PENDIENTE"
                })

            # Confirmar transacción
            con.commit()
            return True, citas_registradas

        except Exception as e:
            con.rollback()
            return False, str(e)

        finally:
            cursor.close()
            con.close()