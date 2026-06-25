from flask import Blueprint, request, jsonify
from models.cita import Cita
from tools.jwt_required import jwt_token_requerido

# Crear módulo Blueprint
ws_cita = Blueprint('ws_cita', __name__)

# Instanciar modelo
modelo = Cita()

# Endpoint para listar las citas de un paciente ("Mis citas")
@ws_cita.route('/citas', methods=['GET'])
@jwt_token_requerido
def listar():
    # Si se envía paciente_id por query string se usa; si no, se resuelve a
    # partir del usuario autenticado (sus propias citas).
    paciente_id = request.args.get("paciente_id")

    if not paciente_id:
        usuario_id = getattr(request, "usuario_id", None)
        paciente_id = modelo.paciente_id_de_usuario(usuario_id)

    if not paciente_id:
        return jsonify({
            'status': False,
            'data': None,
            'message': 'No se pudo determinar el paciente'
        }), 400

    try:
        resultado = modelo.listar_por_paciente(paciente_id)
        return jsonify({
            'status': True,
            'data': resultado,
            'message': 'Citas obtenidas correctamente'
        }), 200
    except Exception as e:
        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500

# Endpoint para registrar una o varias citas
@ws_cita.route('/citas', methods=['POST'])
@jwt_token_requerido
def registrar():
    # Recoger datos
    data = request.get_json()

    paciente_id = data.get("paciente_id")
    paciente_oncologico = data.get("paciente_oncologico", False)
    citas = data.get("citas", [])

    # Usuario autenticado que registra la cita
    # Se asume que el decorador JWT deja disponible request.usuario_id
    creado_por_usuario_id = getattr(request, "usuario_id", None)

    # Validar datos obligatorios
    if not all([paciente_id, citas]):
        return jsonify({
            'status': False,
            'data': None,
            'message': 'Faltan datos obligatorios'
        }), 400

    try:
        estado, resultado = modelo.registrar(
            paciente_id,
            paciente_oncologico,
            creado_por_usuario_id,
            citas
        )

        if estado:
            return jsonify({
                'status': True,
                'data': {
                    'paciente_id': paciente_id,
                    'total_citas_registradas': len(resultado),
                    'citas': resultado
                },
                'message': 'Citas registradas correctamente'
            }), 200
        else:
            return jsonify({
                'status': False,
                'data': None,
                'message': resultado
            }), 500

    except Exception as e:
        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500