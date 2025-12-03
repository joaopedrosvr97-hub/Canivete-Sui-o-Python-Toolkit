# Instalação e Configuração 🛠️

## 📌 Requisitos

Antes de instalar, verifique se possui:

- Python 3.10+
- Git instalado
- Permissão para executar scripts
- Acesso à internet para geolocalização

---

## 📥 1. Clonar o repositório

```sh
git clone https://github.com/joaopedrosvr97-hub/Canivete-Suico-Network-Toolkit

📁 2. Navegar até o projeto

cd Canivete-Suico-Network-Toolkit

🧱 3. Criar ambiente virtual (opcional, recomendado)
python -m venv venv


Ativar ambiente:

Windows:

venv\Scripts\activate


Linux/Mac:

source venv/bin/activate

📦 4. Instalar dependências
pip install -r requirements.txt

▶️ 5. Executar a ferramenta
python src/canivete.py


Tudo pronto 👍


---

# ✅ **📁 3. USAGE – usage.md**

```md
# Guia de Uso ⚙️

A ferramenta é executada diretamente pelo Python:

```sh
python src/canivete.py

📌 Menu interativo

Você verá:

====== CANIVETE SUÍÇO NETWORK TOOLKIT ======

1 - Testar Conexão (Ping)
2 - Coletar Informações da Rede
3 - Geolocalização por IP
4 - Scanner de Dispositivos
5 - Sair

🔹 1. Testar Conexão
python src/canivete.py --ping 8.8.8.8

🔹 2. Coleta de Informações da Rede
python src/canivete.py --info


Isso gera automaticamente um log em:

logs/rede/

🔹 3. Geolocalização por IP
python src/canivete.py --geo 8.8.8.8

🔹 4. Varredura de IPs
python src/canivete.py --scan 192.168.0.0/24

📁 Onde os logs ficam?
logs/
 ├── ping/
 ├── rede/
 ├── geolocation/
 └── scanner/


---

# ✅ **📁 4. MODULES – modules.md**

```md
# Arquitetura dos Módulos 🧩

O projeto usa módulos independentes para facilitar expansão e manutenção.



src/modules/
├── network_info.py
├── ping_test.py
├── geolocation.py
└── scanner.py


---

## 📌 network_info.py
Responsável por:

- Coleta de IP local
- Gateway
- Máscara
- DNS
- Adapters
- Tipo de conexão
- Velocidade de link

---

## 📌 ping_test.py
Executa:

- Teste ping padrão (4 pacotes)
- Interpretação automática do resultado
- Logs com data + IP + tempo médio

---

## 📌 geolocation.py
Consulta APIs de geolocalização pública:

Retorna:

- País
- Cidade
- Região
- Provedor
- Latitude/Longitude

---

## 📌 scanner.py
Responsável por varreduras:

- Scanner ARP
- Scanner ICMP
- Descoberta de dispositivos online
- Registro automático em logs