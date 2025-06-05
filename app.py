from flask import Flask, request, jsonify
from datetime import datetime
from intelbras_api import IntelbrasAccessControlAPI  

app = Flask(__name__)


USE_MOCK = False
DEVICE_IP = 'localhost:8080' if USE_MOCK else '192.168.0.50'
USERNAME = 'admin'
PASSWORD = 'Esdo2025'

# Instância da API
api = IntelbrasAccessControlAPI(DEVICE_IP, USERNAME, PASSWORD)

#Testar Comunicação 
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

@app.route ('/cadastrar_usuario', methods=['POST'])
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
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)