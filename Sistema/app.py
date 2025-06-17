import os
import cv2
import traceback
from flask import Flask, request, jsonify
from datetime import datetime
from intelbras_api import IntelbrasAccessControlAPI
from werkzeug.utils import secure_filename
from flask_cors import CORS


app = Flask(__name__) 
CORS(app)




save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "s_files")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

USE_MOCK = False
DEVICE_IP = 'localhost:8080' if USE_MOCK else '192.168.0.50'
USERNAME = 'admin'
PASSWORD = 'Esdo2025'
 
api = IntelbrasAccessControlAPI(DEVICE_IP, USERNAME, PASSWORD)
 
@app.route('/ping_dispositivo', methods=['POST'])
def ping_dispositivo():
    try:
        resultado = api.get_current_time()
        return jsonify({'status': 'sucesso', 'mensagem': resultado}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500


@app.route('/')
def home():
    return 'API de cadastro facial ativa.'


@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    try:
        user_id = gerar_user_id
        data = request.get_json()
        nome = data.get('nome')
        senha = data.get('senha') or '1234'
        inicio = data.get('inicio') or '2025-01-01 00:00:00'
        fim = data.get('fim') or '2030-01-01 00:00:00'

        resultado = api.add_user_v2(
            CardName=nome,
            UserID=user_id,
            UserType=0,
            Password=senha,
            Authority=2,
            Doors=0,
            TimeSections=255,
            ValidDateStart=inicio,
            ValidDateEnd=fim
        )

        return jsonify({'status': 'sucesso', 'mensagem': resultado}), 201
    except Exception as e:
        print("Erro detalhado: " + str(e))
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

def gerar_user_id():
    now = datetime.now()
    return int(now.strftime("%Y%m%d%H%M%S"))   

@app.route('/listar_usuarios', methods=['GET'])
def listar_usuarios():
    try:
        resultado = api.get_all_users(count=10)
        return jsonify({'status': 'sucesso', 'usuarios': resultado}), 200
    except Exception as e:
        print("Erro Detalhado", e)
        return jsonify({'status': 'Erro', 'mensagem': str(e)}), 500

@app.route('/deletar_todos_usuarios', methods=['DELETE'])
def deletar_todos_usuarios():
    try:
        resultado = api.delete_all_users_v2()
        return jsonify({'status': 'sucesso', 'mensagem': resultado})
    except Exception as e:
        return jsonify({'status': 'Erro', 'mnesagem': str(e)})

@app.route('/validar_biometria', methods=['POST'])
def validar_biometria():
    try:
        if 'imagem' not in request.files:
            return jsonify({'status': 'erro', 'mensagem': 'Imagem não encontrada na requisição.'}), 400

        imagem = request.files['imagem']
        filename = secure_filename("validacao_temp.jpg")
        filepath = os.path.join("s_files", filename)
        imagem.save(filepath)

        # Carrega e tenta identificar rosto
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return jsonify({'status': 'erro', 'mensagem': 'Nenhum rosto detectado.'}), 422

        return jsonify({'status': 'sucesso', 'mensagem': 'Rosto validado com sucesso.'}), 200

    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
