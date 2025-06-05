# 📸 Sistema de Cadastro de Biometria Facial Remoto

Este projeto tem como objetivo facilitar o cadastramento facial remoto de usuários (pais ou visitantes) que desejam acessar unidades escolares. 
A solução permite que o cadastro biométrico facial seja feito por meio de um celular, com posterior integração automática ao controlador de acesso **SS 3532 MF da Intelbras**.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **Flask** – Criação da API Web
- **OpenCV** – Processamento e validação da imagem facial
- **IntelbrasAccessControlAPI** – Comunicação com o SS 3532 MF via comandos CGI
- **Requests** – Requisições HTTP autenticadas
- **Postman** – Testes manuais dos endpoints
- **Figma** – Protótipos de interface
- *(Opcional)* Redis / RabbitMQ – Controle de concorrência e filas futuras

---

## 🧩 Funcionalidades

- Cadastro facial via celular
- Validação de imagem com OpenCV
- Comunicação segura com o dispositivo SS 3532 MF
- Gerenciamento de usuários por integração com o **InControl Web**
- Mock para testes locais da API (sem necessidade do dispositivo físico)

---

## 🖼 Protótipos (UI/UX)

Desenvolvido no Figma:
- Tela de cadastro de usuário
- Tela de instrução para biometria
- Captura facial em tempo real
- Confirmação de cadastro

---

## ⚙️ Estrutura do Projeto


facial_api_flask/
│
├── app.py                      # API principal com Flask
├── intelbras_api.py           # Classe para comandos HTTP com o SS 3532 MF
├── mock_ss3532mf.py           # Simulador local do dispositivo para testes
├── templates/                 # Interface HTML/CSS
├── s_files/                   # Imagens/arquivos salvos localmente
└── README.md

🛠 Como Rodar Localmente

Clone o repositório:

git clone https://github.com/seuusuario/facial-api-flask.git
cd facial-api-flask

Crie e ative o ambiente virtual:

python -m venv env
env\Scripts\activate  # Windows

Instale as dependências:

pip install -r requirements.txt

Execute a API:

python app.py

(Opcional) Inicie o mock:

python mock_ss3532mf.py

📡 Endpoints da API
GET / – Verifica se a API está ativa

POST /cadastrar_usuario – Envia dados + imagem para cadastrar o usuário

📌 Considerações Finais
Este projeto é um MVP em desenvolvimento e faz parte de uma proposta de inovação tecnológica para instituições de ensino.
A solução é escalável, segura e pode ser adaptada para empresas e condomínios.

🔐 Autor e Licença
Desenvolvido por Wendel Samora
