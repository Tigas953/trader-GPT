# ✅ CHECKLIST DE IMPLEMENTAÇÃO — TRADER GPT

Este documento descreve **todas as fases, passos e critérios de validação**
para a implementação do sistema **Trader GPT**, conforme o DVR oficial.

> ⚠️ Regras gerais do projeto:
> - ❌ Nunca avançar de fase com pendências
> - ❌ Nunca misturar fases
> - ✅ Cada fase concluída deve gerar pelo menos um commit
> - ✅ A UI nunca decide lógica — apenas reflete estado interno

---

## 🔹 FASE 0 — FUNDAÇÃO DO PROJETO (BASE TÉCNICA)

### 🎯 Objetivo
Garantir ambiente limpo, versionado e rastreável.

### Checklist
- [ ] Repositório Git criado e acessível
- [ ] Projeto clonado localmente
- [ ] Estrutura de pastas criada conforme DVR
- [ ] `README.md` criado
- [ ] `LICENSE` criado (MIT recomendado)
- [ ] `.gitignore` criado e validado
- [ ] `git status` sem arquivos indesejados
- [ ] Commit realizado: `chore: initial project structure`

### Critério de saída
> Projeto sincronizado com GitHub, sem lixo versionado

---

## 🔹 FASE 1 — CONTRATO DE ESTADO DO SISTEMA (CRÍTICA)

### 🎯 Objetivo
Definir claramente o que o sistema **pode** e **não pode** fazer.

### Checklist
- [ ] Definir enum de **Modo do Sistema**
- [ ] Definir enum de **Estado da IA**
- [ ] Definir enum de **Estado do Trade**
- [ ] Criar classe `StateManager`
- [ ] Definir estado inicial do sistema
- [ ] Definir transições válidas entre estados
- [ ] Bloquear transições ilegais
- [ ] Criar métodos de leitura de estado (read-only)

📁 Arquivo principal:
- `core/state_manager.py`

### Critério de saída
> Estados inválidos são impossíveis de ocorrer por código

**Commit sugerido**

---

## 🔹 FASE 2 — ENGINE (CÉREBRO DO SISTEMA)

### 🎯 Objetivo
Centralizar toda decisão operacional.

### Checklist
- [ ] Criar `engine.py`
- [ ] Implementar métodos de validação:
  - [ ] `can_run_pre_trade()`
  - [ ] `can_run_gestao()`
  - [ ] `can_run_pos_trade()`
- [ ] Implementar eventos:
  - [ ] Ligar / desligar sistema
  - [ ] Abrir trade
  - [ ] Encerrar trade
- [ ] Engine sempre consulta o `StateManager`
- [ ] Engine nunca chama UI ou IA diretamente

📁 Arquivo:
- `core/engine.py`

### Critério de saída
> Nenhuma ação acontece sem passar pelo engine

**Commit sugerido**

---

## 🔹 FASE 3 — TIMER CENTRAL DE EXECUÇÃO

### 🎯 Objetivo
Impedir concorrência, spam de IA e violações de cooldown.

### Checklist
- [ ] Criar Timer Central
- [ ] Definir cooldown mínimo entre análises
- [ ] Bloquear execuções concorrentes
- [ ] Pausar Timer automaticamente:
  - [ ] Durante análise em execução
  - [ ] Durante trade aberto
  - [ ] Em modo Observação
- [ ] Expor status do Timer (somente leitura)

📁 Arquivo sugerido: `core/timer.py`

### Critério de saída
> Duas análises nunca rodam simultaneamente

**Commit sugerido**

---

## 🔹 FASE 4 — MODELOS DE DADOS E LOGS

### 🎯 Objetivo
Criar a **fonte da verdade histórica** do sistema.

### Checklist
- [ ] Criar modelos de dados:
  - [ ] Trade
  - [ ] Análise pré-trade
  - [ ] Gestão de posição
  - [ ] Pós-trade
- [ ] Criar repositórios CSV
- [ ] Escrita apenas em modo append
- [ ] Validação de dados antes de salvar
- [ ] Log de erros do sistema

📁 Arquivos:
- `data/models.py`
- `data/repositories.py`

### Critério de saída
> Toda ação relevante gera persistência confiável

**Commit sugerido**

---

## 🔹 FASE 5 — OCR E CAPTURA DE TELA (SENSOR DO SISTEMA)

### 🎯 Objetivo
Garantir leitura confiável do mercado.

### Checklist
- [ ] Seleção manual da área da tela (OCR preço)
- [ ] Seleção manual da área da tela (imagem para GPT)
- [ ] Persistir coordenadas selecionadas
- [ ] Implementar OCR de preço
- [ ] Implementar captura de tela para IA
- [ ] Validar OCR:
  - [ ] Se inválido → bloquear IA
- [ ] Tratar falhas de captura

📁 Arquivos:
- `ocr/screen_selector.py`
- `ocr/price_reader.py`
- `capture/screen_capture.py`

### Critério de saída
> IA nunca executa com dados incompletos

**Commit sugerido**

---

## 🔹 FASE 6 — IA (ANÁLISE CONTROLADA)

### 🎯 Objetivo
Executar IA **somente dentro das regras do sistema**.

### Checklist
- [ ] Centralizar prompts em `prompts.py`
- [ ] Implementar parser de decisões
- [ ] Implementar:
  - [ ] Análise pré-trade
  - [ ] Gestão de posição
  - [ ] Análise pós-trade
- [ ] Validar formato da resposta da IA
- [ ] Bloquear IA fora do estado permitido

📁 Arquivos:
- `ia/prompts.py`
- `ia/decision_parser.py`
- `ia/analyzer_pre_trade.py`
- `ia/analyzer_gestao.py`
- `ia/analyzer_pos_trade.py`

### Critério de saída
> IA nunca executa fora do contrato de estado

**Commit sugerido**

---

## 🔹 FASE 7 — INTERFACE (UI COMO ESPELHO DO SISTEMA)

### 🎯 Objetivo
A UI apenas reflete o estado real do sistema.

### Checklist
- [ ] Criar janela principal
- [ ] Criar abas vazias
- [ ] Conectar botões ao engine
- [ ] Bloquear ações proibidas visualmente
- [ ] Aplicar semântica correta de cores
- [ ] Exibir estado real da IA
- [ ] Exibir status do Timer

📁 Arquivos:
- `ui/app.py`
- `ui/tabs/*.py`

### Critério de saída
> UI não permite nenhuma ação ilegal

**Commit sugerido**

---

## 🔹 FASE 8 — VALIDAÇÃO OPERACIONAL FINAL

### 🎯 Objetivo
Testar cenários críticos e falhas reais.

### Checklist
- [ ] Troca de modo com sistema ligado
- [ ] OCR falhando
- [ ] Trade aberto + gatilho automático
- [ ] Pós-trade sem dados completos
- [ ] Execuções concorrentes bloqueadas
- [ ] Logs corretos e completos

**Commit sugerido**

---

## 🧠 RESUMO FINAL

### Ordem imutável de implementação
1. Contrato de Estado  
2. Engine  
3. Timer  
4. Dados  
5. OCR / Captura  
6. IA  
7. UI  
8. Validação  

> ❗ Qualquer violação dessa ordem aumenta risco técnico.

---

📌 **Este documento é a referência oficial de execução do projeto Trader GPT.**