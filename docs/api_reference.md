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

🌐 network_info.py
get_network_info() -> dict

Coleta detalhes de rede:

{
  "ip": "192.168.0.10",
  "gateway": "192.168.0.1",
  "mask": "255.255.255.0",
  "dns": ["8.8.8.8", "1.1.1.1"]
}

📍 geolocation.py
geo_ip(ip: str) -> dict

Retorna informações de geolocalização.

🔎 scanner.py
scan_network(range: str) -> list

Escaneia dispositivos online.


---

# ✅ **📁 6. TROUBLESHOOTING – troubleshooting.md**

```md
# Solução de Problemas 🔍

---

## ❗ Erro: "can't open file src/"
Causa:
- Você executou o comando no diretório errado.

Solução:
```sh
cd Canivete-Suico-Network-Toolkit

❗ git push erro: "fetch first"

Você tentou enviar commits com alterações no GitHub.

Solução:

git push -u origin main --force

❗ Ping não funciona

Firewall pode estar bloqueando.

Solução:

execute como administrador

faça teste com outro IP

❗ Scanner lento

Rede pode estar protegida contra ICMP.

Solução:

use faixa menor

evite /24 em redes públicas


---


```md
# Roadmap 🚀

## 🟦 Versão 1.1
- Interface gráfica (GUI)
- Dashboard HTML com resultados
- Exportação PDF dos logs

## 🟪 Versão 1.2
- Teste de portas abertas
- WHOIS lookup
- Detecção de serviços online

## 🟥 Versão 2.0
- API REST
- Sistema de plugins
- Aplicativo mobile para controle remoto

## 🟩 Versão 3.0
- Inteligência de rede (IA)
- Previsão de falhas
- Autocorreção de problemas