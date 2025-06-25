import requests
import os
from datetime import datetime
from requests.auth import HTTPDigestAuth
from PIL import Image




class IntelbrasAccessControlAPI:
    def __init__(self, ip: str, username: str, passwd: str):
        self.ip = ip
        self.username = username
        self.passwd = passwd
        self.digest_auth = requests.auth.HTTPDigestAuth(self.username, self.passwd)
    def get_current_time(self) -> datetime:
        try:
            url = f"http://{self.ip}/cgi-bin/global.cgi?action=getCurrentTime"
            result = requests.get(url, auth=self.digest_auth, timeout=20)
            raw = result.text.strip().splitlines()
            data = self._raw_to_dict(raw)
            return data.get("result", "N/A")
        except Exception as e:
            raise Exception(f"ERROR - During Get Current Time: {str(e)}")
    
    def add_user_v2(self, CardName: str, UserID: int, UserType: int, Password: int, Authority: int, Doors: int, TimeSections: int, ValidDateStart: str, ValidDateEnd: str) -> str:
        ''''
        UserID: Numero de ID do usuário
        CardName: Nome de usuário/Nome do cartão
        UserType: 0- Geral user, by defaut; 1 - Blocklist user (report the blocklist event ACBlocklist); 2 - Guest user: 3 - Patrol user 4 - VIP user; 5 - Disable user
        Password: Senha de acesso do usuário
        Authority: 1 - administrador; 2 - usuário normal
        Doors: Portas que o usúario terá acesso
        TimeSections: Zona de tempo de acesso do usuário, padrão: 255
        ValidDateStart: Data de Inicio de Validade, exemplo: 2019-01-02 00:00:00
        ValidDateEnd: Data de Final de Validade, exemplo: 2037-01-02 01:00:00
        '''
        UserList = (
            '''{
                "UserList": [
                    {
                        "UserID": "''' + str(UserID) + '''",
                        "UserName": "''' + str(CardName) + '''",
                        "UserType": ''' + str(UserType) + ''',
                        "Authority": "''' + str(Authority) + '''",
                        "Password": "''' + str(Password) + '''",
                        "Doors": "''' + '[' + str(Doors) + ']' + '''",
                        "TimeSections": "''' + '[' + str(TimeSections) + ']' + '''",
                        "ValidFrom": "''' + str(ValidDateStart) + '''",
                        "ValidTo": "''' + str(ValidDateEnd) + '''"
                    }
                ]
            }''')
        try:
            url = "http://{}/cgi-bin/AccessUser.cgi?action=insertMulti".format(str(self.ip))
            result = requests.get(url, data=UserList, auth=self.digest_auth, stream=True, timeout=20)

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Add New User using V2 command - ")
    
    def get_all_users(self, count: int) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/recordFinder.cgi?action=doSeekFind&name=AccessControlCard&count={count}"
            result = requests.get(url, auth=self.digest_auth, timeout=20)
            raw = result.text.strip().splitlines()
            return self._raw_to_dict(raw)
        except Exception as e:
            raise Exception(f"ERROR - During Get All User: {str(e)}")

    def delete_all_users_v2(self) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/AccessUser.cgi?action=removeAll"
            result = requests.get(url, auth=self.digest_auth, timeout=20)
            if result.status_code != 200:
                raise Exception(f"Falha ao remover todos os usuários. Status: {result.status_code}")
            return result.text
        except Exception as e:
            raise Exception(f"ERROR - During Remove All Users: {str(e)}")
    
    def _gerar_user_id(self):
        return int(datetime.now().strftime("%Y%m%d%H%M%S"))

    def _raw_to_dict(self, raw):
        data = {}
        for line in raw:
            if "=" in line:
                key, val = line.split("=", 1)
                data[key.strip()] = val.strip()
        return data
    
    def send_face_to_device(self, user_id: int, image_path: str):
        
        url = f"http://{self.ip}/cgi-bin/faceRecognition.cgi?action=uploadFaceImage&UserID={user_id}"

        auth = HTTPDigestAuth(self.username, self.passwd)

        try:
            base, _ = os.path.splitext(image_path)
            converted_path = f"{base}_converted.jpg"

            img = Image.open(image_path).convert("RGB")
            img.save(converted_path, format="JPEG", quality=90)

            with open(converted_path, 'rb') as image_file:
                files = {
                    'FaceImage': ('face.jpg', image_file, 'image/jpeg'),
                }
                response = requests.post(url, files=files, auth=auth, timeout=20)
            if os.path.exists(converted_path):
                os.remove(converted_path)
            
            if response.status_code != 200:
                raise Exception(f"Falha ao enviar rosto: {response.status_code} - {response.text}")
            
            return response.text
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"ERROR - During Upload Face Image: {e}")
        
    def testar_comunicacao(self):
        try:
            url = f"http://{self.ip}/cgi-bin?action=getProductDefiniton"
            response = requests.get(url, auth=HTTPDigestAuth(self.username,self.passwd), timeout=10)
            if response.status_code ==200:
                print("Comunicação e autentificação DIGEST funcionando!")
                print("Resposta:", response.text)
                return True
            else:
                print(f"Erro: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print("Erro de comunicação com o dispositivo:", e)
            return False
        