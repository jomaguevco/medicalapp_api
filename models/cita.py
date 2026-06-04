from conexionBD import Conexion

class Cita:
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