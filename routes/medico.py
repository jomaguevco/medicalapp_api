from flask import Blueprint, request, jsonify, send_from_directory
from models.medico import Medico
from tools.jwt_required import jwt_token_requerido

#Crear un modulo (servicio) para la gestión de médicos
ws_medico = Blueprint('ws_medico', __name__)

medico = Medico()

# ===================== REGISTRAR MÉDICO =====================
@ws_medico.route('/medicos', methods=['POST'])
@jwt_token_requerido
def registrar_medico():
    """Registrar nuevo médico."""
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        nombres = data.get('nombres')
        apellidos = data.get('apellidos')
        dni = data.get('dni')
        cmp = data.get('cmp')
        telefono = data.get('telefono')
        especialidad_id = data.get('especialidad_id')
        horario=data.get('horario')
        consultorio = data.get('consultorio')
        
        if not all([email, password, nombres, apellidos, dni, cmp,telefono,especialidad_id,horario,consultorio]):
            return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
        
        exitoso, resultado = medico.registrar(email, password, nombres, apellidos, dni, cmp, telefono, horario, consultorio, especialidad_id)
        
        if exitoso:
            return jsonify({'status': True, 'data': resultado, 'message': 'Médico registrado correctamente'}), 201
        else:
            return jsonify({'status': False, 'data': None, 'message': resultado}), 400
            
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500

# M.1 Listar médicos
@ws_medico.route('/medicos', methods=["GET"])
@jwt_token_requerido
def listar_medicos():
    try:
        resultado = medico.consultarMedicos()

        data = []
        for row in resultado:
            data.append({
                "id": row["id"],
                "nombre": row["nombre"],
                "especialidad": row["especialidad"],
                "horario": row["horario"],
                "consultorio": row["consultorio"],
                "imagen_url": f"/medicos/{row['id']}/imagen"
            })

        return jsonify({
            'data': data,
            'message': 'Lista de médicos obtenida correctamente',
            'status': True
        }), 200
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500

# M.2 Obtener médico por id
@ws_medico.route('/medicos/<id_medico>', methods=["GET"])
@jwt_token_requerido
def obtener_medico(id_medico):
    if not all([id_medico]):
        return jsonify({'data': None, 'message': 'Faltan datos obligatorios', 'status': False}), 400

    try:
        resultado = medico.obtener_medico_por_id(id_medico)

        if not resultado:
            return jsonify({'data': None, 'message': 'Médico inexistente', 'status': False}), 404

        resultado["imagen_url"] = f"/medicos/{resultado['id']}/imagen"

        return jsonify({
            'data': resultado,
            'message': 'Médico obtenido correctamente',
            'status': True
        }), 200
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500

# M.3 Obtener la imagen del médico
@ws_medico.route('/medicos/<int:id>/imagen', methods=['GET'])
@jwt_token_requerido
def obtener_imagen(id):
    #validar si se cuenta con el id para obtener la foto
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400

    try:
        resultado = medico.obtener_imagen(id)
        if resultado:
            return send_from_directory('uploads/fotos/medicos', resultado['foto'])
        else:
            return send_from_directory('uploads/fotos/medicos', 'default.png')
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
