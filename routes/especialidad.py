from flask import Blueprint,request,jsonify, send_from_directory
from models.especialidad import Especialidad
from tools.jwt_required import jwt_token_requerido

#Crear un modulo (servicio) para la gestión de especialidades
ws_especialidad = Blueprint('ws_especialidad',__name__)

especialidad = Especialidad()

# E.1 Registrar especialidad
@ws_especialidad.route('/especialidades', methods=["POST"])
@jwt_token_requerido
def registrar_especialidad():
    data = request.get_json()
    
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    
    if not all([nombre, descripcion]):
        return jsonify({'data': None, 'message': 'Faltan datos obligatorios', 'status': False}), 400
    
    try:
        esp = Especialidad(nombre=nombre, descripcion=descripcion)
        esp.registrarEspecialidad()
        
        # Obtener el ID generado
        con = __import__('conexionBD').Conexion().open
        cursor = con.cursor()
        cursor.execute("SELECT id FROM especialidad WHERE nombre = %s AND descripcion = %s ORDER BY id DESC LIMIT 1", (nombre, descripcion))
        result = cursor.fetchone()
        cursor.close()
        con.close()
        
        return jsonify({
            'data': {'especialidad_id': result['id']},
            'message': 'Especialidad registrada correctamente',
            'status': True
        }), 201
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500

# E.2 Listar especialidades
@ws_especialidad.route('/especialidades', methods=["GET"])
@jwt_token_requerido
def listar_especialidades():
    try:
        resultado = especialidad.consultarEspecialidades()

        data = []
        for row in resultado:
            data.append({
                "id": row["id"],
                "nombre": row["nombre"],
                "descripcion": row["descripcion"],
                "imagen_url": f"/especialidades/{row['id']}/imagen"
            })
        
        return jsonify({
            'data': data,
            'message': 'Lista de especialidades obtenida correctamente',
            'status': True
        }), 200
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500

# E.3 Obtener especialidad por id
@ws_especialidad.route('/especialidades/<id_especialidad>', methods=["GET"])
@jwt_token_requerido
def obtener_especialidad(id_especialidad):
    if not all([id_especialidad]):
        return jsonify({'data': None, 'message': 'Faltan datos obligatorios', 'status': False}), 400
    
    try:
        resultado = especialidad.obtener_especialidad_por_id(id_especialidad)
        
        if not resultado:
            return jsonify({'data': None, 'message': 'Especialidad inexistente', 'status': False}), 404
        
        return jsonify({
            'data': resultado,
            'message': 'Especialidad obtenida correctamente',
            'status': True
        }), 200
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500

# E.4 Actualizar especialidad
@ws_especialidad.route('/especialidades/<id_especialidad>', methods=["PUT"])
@jwt_token_requerido
def actualizar_especialidad(id_especialidad):
    data = request.get_json()
    
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    
    if not all([nombre, descripcion]):
        return jsonify({'data': None, 'message': 'Faltan datos obligatorios', 'status': False}), 400
    
    try:
        esp = Especialidad(id=id_especialidad, nombre=nombre, descripcion=descripcion)
        esp.actualizarEspecialidad()
        
        return jsonify({
            'data': {'especialidad_id': id_especialidad},
            'message': 'Especialidad actualizada correctamente',
            'status': True
        }), 200
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500

# E.5 Eliminar especialidad
@ws_especialidad.route('/especialidades/<id_especialidad>', methods=["DELETE"])
@jwt_token_requerido
def eliminar_especialidad(id_especialidad):
    if not all([id_especialidad]):
        return jsonify({'data': None, 'message': 'Faltan datos obligatorios', 'status': False}), 400
    
    try:
        esp = Especialidad(id=id_especialidad)
        esp.eliminarEspecialidad()
        
        return jsonify({
            'data': {'especialidad_id': id_especialidad},
            'message': 'Especialidad eliminada correctamente',
            'status': True
        }), 200
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500


# E.6 Obtener la imagen de la especialidad
@ws_especialidad.route('/especialidades/<int:id>/imagen', methods=['GET'])
@jwt_token_requerido
def obtener_imagen(id):
    #validar si se cuenta con el id para obtener la foto
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400

    try:
        resultado = especialidad.obtener_imagen(id)
        if resultado:
            return send_from_directory('uploads/fotos/especialidades', resultado['imagen'])
        else:
            return send_from_directory('uploads/fotos/especialidades', 'default.png')
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500