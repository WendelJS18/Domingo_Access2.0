import requests
import os
from datetime import datetime
from requests.auth import HTTPDigestAuth


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

    def add_user_v2(self, CardName: str, UserType: int, Password: str,
                    Authority: int, Doors: int, TimeSections: int,
                    ValidDateStart: str, ValidDateEnd: str) -> str:
        UserList = {
            "UserList": [
                {
                    "UserName": CardName,
                    "UserID": self._gerar_user_id(),
                    "UserType": UserType,
                    "Authority": Authority,
                    "Password": Password,
                    "Doors": [Doors],
                    "TimeSections": [TimeSections],
                    "ValidFrom": ValidDateStart,
                    "ValidTo": ValidDateEnd
                }
            ]
        }
        try:
            url = f"http://{self.ip}/cgi-bin/AccessUser.cgi?action=insertMulti"
            result = requests.post(url, json=UserList, auth=self.digest_auth, timeout=20)
            if result.status_code != 200:
                raise Exception(f"Falha ao adicionar usuário. Status: {result.status_code}")
            return result.text
        except Exception as e:
            raise Exception(f"ERROR - During Add User V2: {str(e)}")

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
    
    def send_face_to_divice(self, user_id: int, image_path: str):
        
        url = f"http://{self.ip}/cgi-bin/user/UploadFaceImage.cgi"
        auth = HTTPDigestAuth(self.username, self.password)

        try:
            with open(image_path, 'rb') as image_file:
                files = {
                    'FaceImage': image_file,
                }
                data = {
                    'UserID': str(user_id)
                }
                response = requests.post(url, files=files, data=data, auth=auth, timeout=10)
            if response.status_code !=200:
                raise Exception(f"Falha ao enivar rosto: {response.status_code} - {response.text}")
            return response.text
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"ERROR - During Upload Face Image: {e}")

