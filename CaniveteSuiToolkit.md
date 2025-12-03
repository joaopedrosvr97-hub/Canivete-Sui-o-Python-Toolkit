Ferramenta completa de diagnóstico, testes e análise de rede — tudo em um único script.

<p align="center"> <img src="https://img.shields.io/badge/Status-Ativo-32CD32?style=for-the-badge"> <img src="https://img.shields.io/badge/Versão-1.0.0-blue?style=for-the-badge"> <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python"> <img src="https://img.shields.io/badge/Plataforma-Windows%20%7C%20Linux-lightgrey?style=for-the-badge"> <img src="https://img.shields.io/badge/Licença-MIT-purple?style=for-the-badge"> </p>

🔪 Canivete Suíço - PToolKit (GUI)
Uma ferramenta de administração de sistemas multi-plataforma e open source, desenvolvida em Python com interface gráfica (Tkinter), que centraliza funções essenciais de diagnóstico, manutenção e segurança. Ideal para técnicos e administradores que precisam automatizar tarefas repetitivas.

⚠️ Aviso de Segurança e Requisitos
Requisitos
Python 3.x (Recomendado: 3.8 ou superior).

Módulos: tkinter, shutil (inclusos no Python padrão) e pyinstaller (apenas para gerar o executável).

Execução e Privilégios
A maioria das ações deste toolkit (como limpeza de sistema, diagnóstico SFC/DISM e reset de rede) requer privilégios de Administrador (Windows) ou Root (Linux/macOS). O aplicativo solicitará a confirmação para tentar elevar o privilégio, se necessário.

🚀 Como Rodar
1. Clonar o Repositório
Bash

git clone https://github.com/SeuUsuario/canivete-suico-toolkit.git
cd canivete-suico-toolkit
2. Instalar Dependências (Opcional)
A única dependência externa real para rodar é o pyinstaller (se quiser gerar o .exe). Para rodar o código diretamente, não há módulos de terceiros:

Bash

# Apenas se você planeja criar o executável:
pip install pyinstaller
3. Iniciar a Aplicação
Execute o arquivo principal:

Bash

python canivete_gui.py
🛠️ Módulos e Funcionalidades Principais
O toolkit é dividido em seções para fácil navegação e automação de tarefas:

⚙️ Sistema e Diagnóstico
SFC / DISM: Reparos de arquivos de sistema e imagem do Windows.

CHKDSK: Varredura de integridade do disco.

Backup do Registro: Cria cópias de segurança de chaves críticas do Registro do Windows.

Relatório de Desempenho: Inicia o utilitário Perfmon no Windows.

🌐 Rede
Flush DNS: Limpa o cache DNS para resolver problemas de conectividade.

Reset de Rede: Executa comandos como netsh winsock reset e netsh int ip reset.

Coleta de Informações: Captura ipconfig /all, arp -a e rotas.

Ping: Ferramenta de teste de conectividade rápida.

🧹 Limpeza e Otimização
Limpar Temporários: Exclui arquivos temporários do sistema (%TEMP%, C:\Windows\Temp) de forma segura, usando lógica Python (para Unix) ou PowerShell (para Windows).

Otimização de Energia: Aplica perfis de alto desempenho e desativa suspensão.

Desativar Telemetria/Apps: Aplica correções de registro e serviço para limitar dados e desativar recursos indesejados no Windows.

🖨️ Impressão e Spooler
Reiniciar Spooler: Resolve a maioria dos problemas de fila de impressão.

Reparos de Registro: Aplica correções conhecidas de registro relacionadas a problemas de segurança e acesso de impressora.

📈 Visualização Avançada de Saída
Para lidar com a grande quantidade de dados gerados por comandos de sistema (tasklist, netstat, sfc):

Visualizador Tabular: Se a saída se assemelha a dados de coluna (ex: Lista de Processos), é exibida em uma tabela (ttk.Treeview) para facilitar a leitura.

Visualizador de Terminal: Para logs muito longos (> 20.000 caracteres), o resultado é movido para uma janela separada com funções de busca (Ctrl + F) para melhor análise.

🤝 Contribuição
Este projeto é open source e aceita contribuições.

Para reportar bugs ou sugerir funcionalidades, use a seção Issues.

Para submeter código, siga as diretrizes em CONTRIBUTING.md.

⚖️ Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.