# Changelog do Canivete Suíço Toolkit

## [1.0.0] - 2025-12-02 (Versão Inicial)

### Adicionado

* Implementação inicial da aplicação GUI (Tkinter) para administração de sistemas.
* Funcionalidades de Rede (Ping, Flush DNS, Reset).
* Funcionalidades de Impressão (Spooler, Painel, Correções de Registro).
* Funcionalidades de Diagnóstico e Reparo de Sistema (SFC, DISM, CHKDSK).
* Mecanismo de log em arquivo (`logs/`).
* Inclusão de Visualizadores Avançados para saídas longas e tabulares.

### Corrigido

* **action_clean_temp:** Substituída a chamada insegura de 'rm -rf' por lógica Python (`os`, `shutil`) para limpeza de temporários em sistemas Unix/Linux.