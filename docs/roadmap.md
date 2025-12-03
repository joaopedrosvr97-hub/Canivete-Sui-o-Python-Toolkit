# Roadmap — Canivete Suíço Network Toolkit 🚀

**Versão atual:** v1.0.0  
**Última atualização:** 2025-12-02  
**Autor / Maintainer:** João Pedro (joaopedrosvr97-hub)

---

## Visão geral
Este roadmap define a direção técnica e as entregas esperadas para o projeto. Ele está organizado em lançamentos (releases) e em um backlog de médio e longo prazo. Cada item possui prioridade, um breve plano de implementação e critérios de aceitação (Definition of Done — DoD).

---

## Releases previstas

### ✅ v1.0.0 — Lançamento inicial (Concluído)
**Objetivo:** Ter um toolkit estável com funcionalidades básicas e documentação completa.  
**Inclui:**
- Script principal (`src/canivete.py`) com:
  - ping
  - coleta de informações da rede
  - geração de logs
  - menu interativo
- Documentação (`docs/`) e README
- Licença MIT

**DoD:**
- Código testado localmente em Windows e Linux
- README, DOCUMENTACAO.md e docs básicos completados
- Repositório público no GitHub com release criada

---

### 🟡 v1.1.0 — GUI & Melhoria de Logs (Curto prazo)
**Prioridade:** Alta  
**Objetivo:** Entregar interface gráfica básica (Tkinter) e logs em formato estruturado (JSON, com rotação).

**Tarefas principais:**
- [ ] Integrar `canivete_gui.py` ao projeto (src/)
- [ ] Refatorar subsistema de logs para suportar JSON + texto
- [ ] Implementar rotação de logs (max-size / retention)
- [ ] Adicionar botão "Exportar relatório" na GUI

**DoD:**
- GUI inicia em Windows e Linux
- Logs JSON gerados por ações principais
- Testes manuais documentados no `docs/usage.md`

---

### 🔵 v1.2.0 — Scanner de Rede e Portas (Médio prazo)
**Prioridade:** Alta  
**Objetivo:** Adicionar módulos de descoberta (ARP/ping-sweep) e scanner de portas básico (TCP connect).

**Tarefas principais:**
- [ ] Implementar `modules/scanner.py` com:
  - ping-sweep paralelo (threading/async)
  - ARP discovery (quando aplicável)
  - TCP connect para portas comuns (22, 80, 443, 3389)
- [ ] Resultados exportáveis para CSV/JSON
- [ ] Integrar opções no CLI e GUI

**DoD:**
- Scan de /24 completo em tempo aceitável (configurável)
- Resultados consistentes entre CLI e GUI
- Testes de desempenho documentados

---

### 🔷 v2.0.0 — Dashboard Web & API (Longo prazo)
**Prioridade:** Média  
**Objetivo:** Criar painel web para visualização em tempo real e API REST para controlar o toolkit remotamente.

**Tarefas principais:**
- [ ] Criar backend Flask/FastAPI que consome logs e expõe endpoints
- [ ] Criar frontend simples (React / plain HTML) para visualizar:
  - dispositivos ativos
  - histórico de pings
  - alertas
- [ ] Autenticação básica (token) para API

**DoD:**
- Dashboard funcional em localhost
- Endpoints documentados no `docs/api_reference.md`
- Suporte a websockets ou polling para atualização em tempo real

---

### 🟩 v2.1.0+ — Publicação & Ecosistema
**Prioridade:** Baixa → Média  
**Objetivo:** Tornar o projeto instalável via pip, criar release management e CI/CD.

**Tarefas principais:**
- [ ] Estruturar pacote Python (setup.py / pyproject.toml)
- [ ] Publicar no PyPI (nome: `canivete-suico-toolkit` — verificar disponibilidade)
- [ ] Criar GitHub Actions:
  - lint (flake8)
  - unit tests (pytest)
  - build & release automatizado (on tag)
- [ ] Criar CHANGELOG semântico (Keep a Changelog)

**DoD:**
- `pip install canivete-suico-toolkit` instala o pacote
- CI rodando em push e PR
- Releases automatizadas por tag

---

## Backlog / Possíveis Features (ideias)
- Integração com Power BI / exportadores CSV prontos para BI
- Módulo de alertas (email/Telegram/Slack)
- Módulo WHOIS e lookup de ASN
- Integração com Nmap para escaneamento avançado (opcional)
- Versão mobile ou controle remoto via API
- Suporte multiusuário e logs centralizados (ELK / Loki)

---

## Kanban — Sugestão de Colunas e Prioridades
No GitHub Projects, crie um board com colunas:

- Backlog (ideias)
- To do (priorizadas)
- In progress
- Review / QA
- Done

Priorizar issues com labels:
- `priority:high` | `priority:medium` | `priority:low`
- `type:bug` | `type:feature` | `type:docs`
- `area:gui` | `area:cli` | `area:scanner` | `area:logs` | `area:api`

---

## Como transformar itens do roadmap em Issues (modelo)

**Título:** `feature: adicionar scanner de portas básico`  
**Descrição:**
