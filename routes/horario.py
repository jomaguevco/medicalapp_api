from flask import Blueprint, request, jsonify
from models.horario_disponible import HorarioDisponible
from tools.jwt_required import jwt_token_requerido

# Crear un modulo (servicio) para la gestion de horarios disponibles
ws_horario = Blueprint('ws_horario', __name__)

horario = HorarioDisponible()


# H.1 Listar horarios disponibles por especialidad y (opcional) rango de fechas
@ws_horario.route('/horarios-disponibles', methods=["GET"])
@jwt_token_requerido
def listar_horarios_disponibles():
    especialidad_id = request.args.get('especialidad_id')
    desde = request.args.get('desde')   # formato YYYY-MM-DD (opcional)
    hasta = request.args.get('hasta')   # formato YYYY-MM-DD (opcional)

    if not especialidad_id:
        return jsonify({
            'data': None,
            'message': 'Falta el parametro especialidad_id',
            'status': False
        }), 400

    try:
        resultado = horario.consultar_disponibles(especialidad_id, desde, hasta)

        return jsonify({
            'data': resultado,
            'message': 'Lista de horarios disponibles obtenida correctamente',
            'status': True
        }), 200
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500
