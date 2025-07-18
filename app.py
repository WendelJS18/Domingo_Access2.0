import os
import cv2
import traceback
import base64
import logging
from logging.handlers import RotatingFileHandler
from threading import Lock
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime
from Sistema.intelbras_api import IntelbrasAccessControlAPI
from flask_cors import CORS


app = Flask(__name__, 
            template_folder='templates', 
            static_folder='static')
CORS(app)


log_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'domingos_acess.log'

my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app.logger.addHandler(my_handler)
app.logger.setLevel(logging.INFO)

DEVICE_IP = '192.168.137.2'
USERNAME = 'admin'
PASSWORD = 'Esdo2025'

api = IntelbrasAccessControlAPI(DEVICE_IP, USERNAME, PASSWORD)

app.logger.info("API DomingosAccess iniciada com sucesso.")

save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "s_files")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

app.secret_key = 'Domingos@@@@19301'


user_id_lock = Lock()
current_user_id = 1

def gerar_user_id():
    id_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "ultimo_id.txt")

    with user_id_lock:
        if not os.path.exists(id_path):
            with open(id_path, "w") as f:
                f.write("1")

        with open(id_path, "r") as f:
            last_id = int(f.read().strip())

        new_id = last_id + 1

        with open(id_path, "w") as f:
            f.write(str(new_id))

    return str(new_id)

@app.route('/', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            cpf = request.form.get('cpf')
            matricula = request.form.get('matricula')

            app.logger.info(
                f"Recebida tentativa de cadastro para: {nome}, CPF: {cpf}")

           
            #A API DA KINTO
          

            user_id = gerar_user_id()

            resultado = api.add_user_v2(
                CardName=nome,
                UserID=user_id,
                ValidDateStart='2024-01-01 00:00:00',
                ValidDateEnd='2037-12-31 23:59:59',
                UserType=0, Password='Password@123', Authority=2,
                Doors=1, TimeSections=255
            )

            app.logger.info(
                f"Usuário '{nome}' (ID: {user_id}) criado no dispositivo. Redirecionando para captura.")
            return redirect(url_for('captura_page', user_id=user_id, user_name=nome))

        except Exception as e:
            app.logger.error(
                f"Falha na Etapa 1 (Cadastro): {e}", exc_info=True)

            flash(
                'Ocorreu um erro ao comunicar com o dispositivo. Tente novamente.', 'danger')
            return redirect(url_for('cadastrar_usuario'))

    return render_template('index.html')


@app.route('/captura')
def captura_page():
    return render_template('captura.html')


@app.route('/cadastro_sucesso')
def cadastro_sucesso():
    return "<h1>Cadastro realizado com sucesso!</h1><p>Pode fechar esta página.</p>"


@app.route('/ping_dispositivo', methods=['POST'])
def ping_dispositivo():
    try:
        resultado = api.get_current_time()
        return jsonify({'status': 'sucesso', 'mensagem': resultado}), 200
    except Exception as e:
        app.logger.error(
            f"Ocorreu um erro não esperado ao cadastrar usuário: {e}", exc_info=True)
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500

@app.route('/listar_usuarios', methods=['GET'])
def listar_usuarios():
    try:
        resultado = api.get_all_users(count=10)
        return jsonify({'status': 'sucesso', 'usuarios': resultado}), 200
    except Exception as e:
        app.logger.error(f"Ocorreu um erro não ao cadastrar usuário: {e}")
        return jsonify({'status': 'Erro', 'mensagem': str(e)}), 500


@app.route('/deletar_todos_usuarios', methods=['DELETE'])
def deletar_todos_usuarios():
    try:
        resultado = api.delete_all_users_v2()

        with user_id_lock:

            current_user_id = 1

        return jsonify({'status': 'sucesso', 'mensagem': resultado})
    except Exception as e:
        app.logger.error(
            f'Ocorreu um erro não esperado ao deletar todos os usuarios: {e}')
        return jsonify({'status': 'Erro', 'mnesagem': str(e)})


@app.route("/enviar_foto_dispositivo", methods=["POST"])
def enviar_foto_dispositivo():
    filepath = None
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        photo_base64 = data.get("photo_base64")

        if not user_id or not photo_base64:
            return jsonify({"erro": "Dados ausentes (user_id ou photo_base64)."}), 400

        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_upload")
        os.makedirs(temp_dir, exist_ok=True)
        
        from PIL import Image
        from io import BytesIO
        
        img_data = base64.b64decode(photo_base64)
        img = Image.open(BytesIO(img_data)).convert("RGB")
        
        filepath = os.path.join(temp_dir, f"{user_id}_captura.jpg")
        img.save(filepath, format="JPEG")

        resultado = api.send_face_to_device(user_id=user_id, image_path=filepath)
        app.logger.info(f"Foto para o User ID {user_id} enviada com sucesso para o dispositivo.")
        
        return jsonify({"resultado": resultado})

    except Exception as e:
        app.logger.error(f"Falha ao enviar foto para o dispositivo: {e}", exc_info=True)
        return jsonify({"erro": str(e)}), 500
    finally:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":

    app.run(debug=False, host="0.0.0.0")
