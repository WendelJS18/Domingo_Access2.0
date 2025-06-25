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


DEVICE_IP = '192.168.137.2'
USERNAME = '*'
PASSWORD = '*'
 
api = IntelbrasAccessControlAPI(DEVICE_IP, USERNAME, PASSWORD)
api.testar_comunicacao()

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
        user_id = gerar_user_id()
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
        import traceback
        traceback.print_exc()
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
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'Erro', 'mensagem': str(e)}), 500

@app.route('/deletar_todos_usuarios', methods=['DELETE'])
def deletar_todos_usuarios():
    try:
        resultado = api.delete_all_users_v2()
        return jsonify({'status': 'sucesso', 'mensagem': resultado})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'Erro', 'mnesagem': str(e)})

@app.route("/enviar_foto_dispositivo", methods=["POST"])
def enviar_foto_dispositivo():
    try:
        user_id = request.form.get("user_id")
        foto = request.files.get("foto")

        if not user_id or not foto:
            return jsonify({"erro": "Parâmetros obrigatórios ausentes."}), 400

        filepath = os.path.join("temp_upload", foto.filename)
        os.makedirs("temp_upload", exist_ok=True)
        foto.save(filepath)

        resultado = api.send_face_to_device(user_id=user_id, image_path=filepath)

        os.remove(filepath)
        return jsonify({"resultado": resultado})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    
    app.run(debug=False, host="0.0.0.0")