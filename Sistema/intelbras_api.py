from os.path import abspath, dirname, join
import requests
from datetime import datetime


# diretorio para salvar imagens
save_dir = join(dirname(abspath(__file__)), "s_files")


class IntelbrasAccessControlAPI:
    def __init__(self, ip: str, username: str, passwd: str):
        self.ip = ip
        self.username = username
        self.passwd = passwd
        self.digest_auth = requests.auth.HTTPDigestAuth(
            self.username, self.passwd)

    ##### Device Manager #####
    def get_current_time(self) -> datetime:
        try:
            url = url = f"http://{self.ip}/cgi-bin/global.cgi?action=getCurrentTime"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            date_time_obj = datetime.strptime(
                data.get('result').replace(
                    "-", "/"), '%Y/%m/%d %H:%M:%S')

            if result.status_code != 200:
                raise Exception()
            return date_time_obj
        except Exception:
            raise Exception("ERROR - During Get Current Time")

    def set_current_time(self) -> str:
        try:
            current_datetime = datetime.today().strftime('%Y-%m-%d') + '%20' + \
                datetime.today().strftime('%H:%M:%S')

            url = f"http://{self.ip}/cgi-bin/global.cgi?action=setCurrentTime&time={current_datetime}"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Current Time")

    def get_ntp_config(self) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=getConfig&name=NTP"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            raw = result.text.strip().splitlines()

            ntp_config = self._raw_to_dict(raw)

            if result.status_code != 200:
                raise Exception()
            return ntp_config
        except Exception:
            raise Exception("ERROR - During Get NTP Config")

    def set_ntp_config(self, address: str, port: str, enable: bool) -> str:
        try:
            url = (
                f"http://{self.ip}/cgi-bin/configManager.cgi?"
                f"action=setConfig&NTP.Address={address}&NTP.Port={port}&NTP.Enable={str(enable).lower()}")
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set NTP Config")

    def get_software_version(self) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/magicBox.cgi?action=getSoftwareVersion"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            firmware_version = data.get('version')

            if result.status_code != 200:
                raise Exception()
            return firmware_version
        except Exception:
            raise Exception("ERROR - During Get Software Version")

    def get_network_config(self) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=getConfig&name=Network"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            network_config_dict = data

            if result.status_code != 200:
                raise Exception()
            return network_config_dict
        except Exception:
            raise Exception("ERROR - During Get Network Config")

    def get_device_serial(self) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/magicBox.cgi?action=getSerialNo"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            device_serial = data.get('sn')

            if result.status_code != 200:
                raise Exception()
            return device_serial
        except Exception:
            raise Exception("ERROR - During Get Device Serial")

    def get_cgi_version(self) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/IntervideoManager.cgi?action=getVersion&Name=CGI"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            cgi_version = data.get('version')

            if result.status_code != 200:
                raise Exception()
            return cgi_version
        except Exception:
            raise Exception("ERROR - During Get CGI Version")

    def get_device_type(self) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/magicBox.cgi?action=getSystemInfo"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            device_type = data.get('deviceType')

            if result.status_code != 200:
                raise Exception()
            return device_type
        except Exception:
            raise Exception("ERROR - During Get Device Type")

    def set_network_config(
            self,
            new_ip: str,
            new_gateway: str,
            new_mask: str,
            dhcp: bool) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&Network.eth0.IPAddress={new_ip}&Network.eth0.DefaultGateway={new_gateway}&Network.eth0.SubnetMask={new_mask}&Network.eth0.DhcpEnable={ str(dhcp).lower()}"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Network Config")

    def reboot_device(self) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/magicBox.cgi?action=reboot"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Reboot Device")

    ##### Event Server Manager #####
    def set_event_sender_configuration(
            self,
            state: bool,
            server_address: str,
            port: int,
            path: str) -> str:
        '''
        state: True / False
        server_address: Endereço de IP ou DDNS do servidor
        port: Porta do Servidor
        path: Path do servidor, exemplo /notification
        '''
        try:

            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&PictureHttpUpload.Enable={str(state).lower()}&PictureHttpUpload.UploadServerList[0].Address={server_address}&PictureHttpUpload.UploadServerList[0].Port={port}&PictureHttpUpload.UploadServerList[0].Uploadpath={path}"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Current Time")

    ##### Door Config #####
    def open_door(self, door: int) -> str:
        '''
        Send a remote command to open door, default value for door is 1
        '''
        try:
            url = f"http://{self.ip}/cgi-bin/accessControl.cgi?action=openDoor&channel={door}"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Open Door - ", e)

    def close_door(self, door: int) -> str:
        '''
        Send a remote command to open close, default value for door is 1
        '''
        try:
            url = f"http://{self.ip}/cgi-bin/accessControl.cgi?action=closeDoor&channel={door}"

            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Close Door - ", e)

    def set_door_state(self, state: int) -> str:
        '''
        0 = Normal/Estado normal de porta
        1 = CloseAlways/Porta sempre fechada
        2 = OpenAlways/Porta sempre aberta
        '''
        try:
            estado = ['Normal', 'CloseAlways', 'OpenAlways']
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].State={str(estado[state])}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Door State")

    def set_door_sensor_delay(self, CloseTimeout: int) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].CloseTimeout={CloseTimeout}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Door Sensor Delay")

    def set_door_sensor_state(self, SensorType: int) -> str:
        '''
        0 = Sempre Aberto
        1 = Sempre Fechado
        '''
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControlGeneral.SensorType={SensorType}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Door Sensor State")

    def set_door_name(self, Name: str) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].Name={Name}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Door Name")

    def enable_door_sensor(self, SensorEnable: bool) -> str:
        try:

            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].SensorEnable={str(SensorEnable).lower()}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Enable Door Sensor ")

    def set_door_unlock_interval(self, UnlockHoldInterval: int) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].UnlockHoldInterval={UnlockHoldInterval}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Set Unlock Interval")

    def enable_exit_button(self, ButtonExitEnable: bool) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControlGeneral.ButtonExitEnable={str(ButtonExitEnable).lower()}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Enable/Disable Exit Button")

    def set_door_verification_method(self, Method: int) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].Method={Method}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During set Door Verification Method")

    def set_open_timezone(self, OpenAlwaysTime: int) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].OpenAlwaysTime={OpenAlwaysTime}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Open Timezone")

    def set_close_timezone(self, CloseAlwaysTime: int) -> str:
        try:
            url = f"http://1{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].CloseAlwaysTime={CloseAlwaysTime}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Close Timezone")

    def get_door_config(self) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=getConfig&name=AccessControlGeneral"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Door Config")

    def get_door_state(self, door: int) -> str:
        '''
        Return Close or Open to Door State
        '''
        try:
            url = f"http://{self.ip}/cgi-bin/accessControl.cgi?action=getDoorStatus&channel={door}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            door_state = data.get('Info.status')

            if result.status_code != 200:
                raise Exception()
            return str(door_state)
        except Exception as e:
            raise Exception("ERROR - During Get Door State - ", e)

    def set_access_control_door_enable(self, state: bool) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AccessControl[0].Enable={str(state).lower()}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Enable Door - ", e)

    def stop_alarm_v2(self) -> str:
        try:
            url = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&AlarmStop.stopAlarm=true"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception("ERROR - During Stop Alarm V2 ", e)

# User Manager

    def delete_all_users_v1(self) -> str:
        '''
        This command delete all user and credential incluse in device
        '''
        try:
            url = f"http://{self.ip}/cgi-bin/recordUpdater.cgi?action=clear&name=AccessControlCard"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception(
                "ERROR - During Remove All Users using V1 command - ", e)

    def delete_all_users_v2(self) -> str:
        '''
        This command delete all user and credential incluse in device
        '''
        try:
            url = f"http://{self.ip}/cgi-bin/AccessUser.cgi?action=removeAll"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception as e:
            raise Exception(
                "ERROR - During Remove All Users using V2 command - ", e)

    def add_user_v1(
            self,
            CardName: str,
            UserID: int,
            CardNo: str,
            CardStatus: int,
            CardType: int,
            Password: int,
            Doors: int,
            ValidDateStart: datetime,
            ValidDateEnd: datetime) -> dict:
        '''
        CardName: Nome do Usuário / Nome do Cartão
        UserId: Numero de ID do Usuário
        CardNo: Código Hexadecimal do Cartão
        CardStatus:  0 = Normal, 1 = Cancelado, 2 = Congelado
        CardType: 0 = Ordinary card, 1 = VIP card, 2 = Guest card, 3 = Patrol card, 4 = Blocklist card, 5 = Duress card
        Password: Senha de Acesso, Min 4 - Max 6
        Doors: Portas de Acesso, Default 0
        '''
        start_time_str = ValidDateStart.strftime(
            '%Y-%m-%d') + '%20' + ValidDateStart.strftime('%H:%M:%S')
        end_time_str = ValidDateEnd.strftime(
            '%Y%m%d') + '%20' + ValidDateEnd.strftime('%H%M%S')
        try:
            url = (
                f"http://{self.ip}/cgi-bin/recordUpdater.cgi?action=insert&name=AccessControlCard"
                f"&CardNo={CardNo.upper()}"
                f"&CardStatus={CardStatus}"
                f"&CardName={CardName}"
                f"&UserID={UserID}"
                f"&Password={Password}"
                f"&CardType={CardType}"
                f"&Doors[0]={Doors}"
                f"&ValidDateStart={start_time_str}"
                f"&ValidDateEnd={end_time_str}"
            )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)

            if result.status_code != 200:
                raise Exception()
            return data
        except Exception as e:
            raise Exception(
                "ERROR - During Add New User using V1 command - ", e)

    def add_user_v2(
            self,
            CardName: str,
            UserID: int,
            UserType: int,
            Password: int,
            Authority: int,
            Doors: int,
            TimeSections: int,
            ValidDateStart: str,
            ValidDateEnd: str) -> str:
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
            url = f"http://{self.ip}/cgi-bin/AccessUser.cgi?action=insertMulti"
            headers = {"Content-TYpe": "application/json"}
            result = requests.post(
                url,
                data=UserList,
                headers=headers,
                auth=self.digest_auth,
                timeout=20,
                verify=False)

            return result.text

        except Exception as e:
            raise Exception(
                f"ERROR - During Add New User using V2 command - {str(e)}")

            if result.status_code != 200:
                raise Exception(
                    f"Falha ao adicionar usuário. Código de status: {result.status_code}. Resposta: {result.text}")

    def update_user_v2(
            self,
            CardName: str,
            UserID: int,
            UserType: int,
            Password: int,
            Authority: int,
            Doors: int,
            TimeSections: int,
            ValidDateStart: str,
            ValidDateEnd: str) -> str:
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
                            "UserName": "''' + str(CardName) + '''",
                            "UserID": "''' + str(UserID) + '''",
                            "UserType": ''' + str(UserType) + ''',
                            "Password": "''' + str(Password) + '''",
                            "Authority": "''' + str(Authority) + '''",
                            "Doors": "''' + '[' + str(Doors) + ']' + '''",
                            "TimeSections": "''' + '[' + str(TimeSections) + ']' + '''",
                            "ValidFrom": "''' + str(ValidDateStart) + '''",
                            "ValidTo": "''' + str(ValidDateEnd) + '''"
                        }
                    ]
                }''')
        try:
            url = f"http://{self.ip}/cgi-bin/AccessUser.cgi?action=updateMulti"

            result = requests.get(url, data=UserList, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Update User using V2 command - ")

    def get_all_users(self, count: int) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/recordFinder.cgi?action=doSeekFind&name=AccessControlCard&count={count}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users")

    def get_users_count(self) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/recordFinder.cgi?action=getQuerySize&name=AccessUserInfo"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users Count")

    def get_user_cardno(self, CardNoList: str) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/AccessCard.cgi?action=list&CardNoList[0]={str(CardNoList).upper()}".format(
                str(self.ip), str(CardNoList).upper(), )
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users CardNo")

    def get_user_recno(self, recno: int) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/recordUpdater.cgi?action=get&name=AccessControlCard&recno={recno}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users RecNo")

    def get_user_id(self, UserIDList: int) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/AccessUser.cgi?action=list&UserIDList[0]={UserIDList}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Get Users Id")

    def set_remove_users_all(self) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/recordUpdater.cgi?action=clear&name=AccessControlCard"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Remove All Users")

    def set_remove_users_recno(self, recno: int) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/recordUpdater.cgi?action=remove&name=AccessControlCard&recno={recno}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Remove Users By RecNo")

    def set_remove_users_id(self, UserIDList: int) -> dict:
        try:
            url = f"http://{self.ip}/cgi-bin/AccessUser.cgi?action=removeMulti&UserIDList[0]={UserIDList}"
            result = requests.get(url, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa
            raw = result.text.strip().splitlines()

            data = self._raw_to_dict(raw)
            if result.status_code != 200:
                raise Exception()
            return data
        except Exception:
            raise Exception("ERROR - During Remove Users By ID")

    def add_card_v2(
            self,
            UserID: int,
            CardNo: str,
            CardType: int,
            CardStatus: int) -> dict:
        '''
        UserID: ID do usuário
        CardNo: Número do cartão
        CardType: Tipo do Cartão; 0- Ordinary card; 1- VIP card; 2- Guest card; 3- Patrol card; 4- Blocklist card; 5- Duress card
        CardStatus: Status do Cartão; 0- Normal; 1- Cancelado; 2- Congelado
        '''
        CardList = (

            '''{
                    "CardList": [
                        {
                            "UserID": "''' + str(UserID) + '''",
                            "CardNo": "''' + str(CardNo) + '''",
                            "CardType": ''' + str(CardType) + ''',
                            "CardStatus": "''' + str(CardStatus) + '''"
                        }
                    ]
                }''')

        try:
            url = f"http://{self.ip}/cgi-bin/AccessCard.cgi?action=insertMulti".format(
                f"&UserID = {UserID}"
                f"&CardNo = {(CardNo).upper()}"
                f"&CardType = {CardNo}"
                f"&CardStatus = {CardStatus}"
            )
            result = requests.post(url, data=CardList, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result.status_code != 200:
                raise Exception()
            return str(result.text)
        except Exception:
            raise Exception("ERROR - During Add Card")

    def config_online_mode(
            self,
            enable,
            server_address,
            port,
            path_event,
            device_mode,
            enable_keepalive,
            interval_keepalive,
            path_keepalive,
            timeout_keepalive,
            timeout_response) -> bool:
        try:

            url_server_config = "http://{}/cgi-bin/configManager.cgi?action=setConfig&PictureHttpUpload.Enable={}&PictureHttpUpload.UploadServerList[0].Address={}&PictureHttpUpload.UploadServerList[0].Port={}&PictureHttpUpload.UploadServerList[0].Uploadpath={}".format(
                str(self.ip),
                str(enable),
                str(server_address),
                str(port),
                str(path_event),
            )

            url_keepalive_config = f"http://{self.ip}/cgi-bin/configManager.cgi?action=setConfig&Intelbras_ModeCfg.DeviceMode={device_mode}&Intelbras_ModeCfg.KeepAlive.Enable={enable_keepalive}&Intelbras_ModeCfg.KeepAlive.Interval={interval_keepalive}&Intelbras_ModeCfg.KeepAlive.Path={path_keepalive}&Intelbras_ModeCfg.KeepAlive.TimeOut={timeout_keepalive}&Intelbras_ModeCfg.RemoteCheckTimeout={timeout_response}"

            result_events = requests.get(url_server_config, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            result_keepalive = requests.get(url_keepalive_config, auth=self.digest_auth, stream=True, timeout=20, verify=False)  # noqa

            if result_events.status_code != 200 or result_keepalive.status_code != 200:
                raise Exception()
            return str(result_events.text)
        except Exception:
            raise Exception("ERROR - During Set Online Mode")

    def _raw_to_dict(self, raw):
        data = {}
        for i in raw:
            if len(i) > 1:
                name = i[:i.find("=")]
                val = i[i.find("=") + 1:]
                try:
                    len(data[name])
                except BaseException:
                    data[name] = val
            else:
                data["NaN"] = "NaN"
        return data
    
    def send_face_to_device(self, user_id: int, image_path: str) -> str:
    
      try:
        url = f"http://{self.ip}/cgi-bin/faceRecognition.cgi?action=uploadFaceImage&UserID={user_id}"

        with open(image_path, 'rb') as img_file:
            files = {'FaceImage': (f"user_{user_id}.jpg", img_file, 'image/jpeg')}
            result = requests.post(url, files=files, auth=self.digest_auth, timeout=20, verify=False)

        if result.status_code != 200:
            raise Exception(f"Falha ao enviar rosto: {result.status_code} - {result.text}")
        return result.text

      except Exception as e:
        raise Exception(f"ERROR - During Upload Face Image: {e}")
    

            


# api.get_current_time()
