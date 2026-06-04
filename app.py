from flask import Flask
from routes.usuario import ws_usuario
from routes.especialidad import ws_especialidad
from routes.cita import ws_cita
from routes.medico import ws_medico

app = Flask(__name__)
app.register_blueprint(ws_usuario, url_prefix='/api')
app.register_blueprint(ws_especialidad, url_prefix='/api')
app.register_blueprint(ws_cita, url_prefix='/api')
app.register_blueprint(ws_medico, url_prefix='/api')

@app.route('/')
def home():
    return 'MedicalApp - Running API Restful'


#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=3007, debug=True, host='0.0.0.0')