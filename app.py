import os
import cv2
from flask import Flask, request, jsonify
from datetime import datetime
from intelbras_api import IntelbrasAccessControlAPI
from werkzeug.utils import secure_filename

app = Flask(__name__)


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
        print("Erro detalhado:", e)
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500


@app.route('/')
def home():
    return 'API de cadastro facial ativa.'


@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    try:
        data = request.get_json()
        nome = data.get('nome')
        user_id = data.get('user_id')
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


@app.route('/upload_foto', methods=['POST'])
def upload_foto():
    try:
        if 'imagem' not in request.files:
            return jsonify({'status': 'erro', 'mensagem': 'Nenhum arquivo enviado com chave "imagem".'}), 400

        imagem = request.files['imagem']
        user_id = request.form.get('user_id')

        if not user_id:
            return jsonify({'status': 'erro', 'mensagem': 'O campo "user_id" é obrigatório.'}), 400

        # Cria diretório se não existir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Nome seguro do arquivo
        filename = secure_filename(f"user_{user_id}.jpg")
        filepath = os.path.join(save_dir, filename)

        imagem.save(filepath)

        return jsonify({'status': 'sucesso', 'mensagem': 'Imagem salva com sucesso.', 'caminho': filepath}), 201

    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500


@app.route('/recortar_rosto', methods=['POST'])
def recortar_rosto():
    try:
        user_id = request.json.get('user_id')

        if not user_id:
            return jsonify({'status': 'erro', 'mensagem': 'O campo "user_id" é obrigatório.'}), 400

        filename = f"user_{user_id}.jpg"
        filepath = os.path.join(save_dir, filename)

        if not os.path.exists(filepath):
            return jsonify({'status': 'erro', 'mensagem': 'Imagem não encontrada.'}), 404

        # Carregar imagem
        imagem = cv2.imread(filepath)
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        # Classificador Haar
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            return jsonify({'status': 'erro', 'mensagem': 'Nenhum rosto detectado.'}), 422

        # Assumir primeiro rosto encontrado
        (x, y, w, h) = faces[0]
        rosto = imagem[y:y + h, x:x + w]

        # Salvar rosto recortado no mesmo local
        cv2.imwrite(filepath, rosto)

        return jsonify({'status': 'sucesso', 'mensagem': 'Rosto recortado com sucesso.'}), 200

    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
