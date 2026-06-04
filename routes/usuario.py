from flask import Blueprint, request, jsonify, send_from_directory
from models.usuario import Usuario
from tools.jwt_utils import generar_token
from tools.jwt_required import jwt_token_requerido

#Crear un módulo (servicio) para la gestión de usuarios: login, registro, cambiar contraseña
ws_usuario = Blueprint('ws_usuario', __name__)

#Instanciar al usuario
usuario = Usuario()

# A.1 Login
@ws_usuario.route('/login', methods=['POST'])
def login():
    #Obtener las credenciales que se recibe como dato de entrada
    data = request.get_json()
    
    #Almacenar las credenciales en variables locales
    email = data.get('email')
    password = data.get('password')
    
    #Validar si contamos con las credenciales
    if not all([email, password]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    #Ejecutar el inicio de sesión
    try:
        #Llamar al método login
        resultado = usuario.login(email, password)
        
        if resultado: #Validar si hay resultado
            #Retirar la clave del resultado
            resultado.pop ('password', None)
            
            #Generar el token JWT
            token = generar_token({'usuario_id': resultado['usuario_id']}, 60*60)
            
            #Incluir el token en el resultado del endpoint
            resultado['token'] = token
            
            
            #Imprimir el resultado
            return jsonify({'status': True, 'data': resultado, 'message': 'Inicio de sesión satisfactorio'}), 200
        
        else: #Credenciales incorrectas
            return jsonify({'status': False, 'data': None, 'message': 'Credenciales incorrectas'}), 401
            
        
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500


# A.2 Perfil del usuario autenticado
@ws_usuario.route('/perfil', methods=["GET"])
@jwt_token_requerido
def perfil():
    try:
        usuario_id = request.usuario_id
        resultado = usuario.obtener_perfil(usuario_id)
        
        if not resultado:
            return jsonify({'status': False, 'data': None, 'message': 'Usuario inexistente'}), 404
        
        return jsonify({
            'status': True,
            'data': resultado,
            'message': 'Perfil obtenido correctamente'
        }), 200
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    

# A.3 Obtener foto del usuario
@ws_usuario.route('/usuarios/foto/<id>', methods=['GET'])
@jwt_token_requerido
def obtener_foto(id):
    #validar si se cuenta con el id para obtener la foto
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400

    try:
        resultado = usuario.obtener_foto(id)
        if resultado:
            return send_from_directory('uploads/fotos/usuarios', resultado['foto'])
        else:
            return send_from_directory('uploads/fotos/usuarios', 'default.png')
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500