import os
from flask import Flask
from routes.usuario import ws_usuario
from routes.especialidad import ws_especialidad
from routes.cita import ws_cita
from routes.medico import ws_medico
from routes.horario import ws_horario

app = Flask(__name__)
app.register_blueprint(ws_usuario, url_prefix='/api')
app.register_blueprint(ws_especialidad, url_prefix='/api')
app.register_blueprint(ws_cita, url_prefix='/api')
app.register_blueprint(ws_medico, url_prefix='/api')
app.register_blueprint(ws_horario, url_prefix='/api')

@app.route('/')
def home():
    return 'MedicalApp - Running API Restful'


#Iniciar el servicio web con Flask (solo para ejecucion local).
#En produccion lo arranca gunicorn (ver Procfile).
if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 3007))
    app.run(port=puerto, debug=True, host='0.0.0.0')