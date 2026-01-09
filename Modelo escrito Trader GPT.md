====================================================================
DOCUMENTO DE VISÃO E REQUISITOS (DVR)
PROJETO DE SOFTWARE — TRADER GPT
====================================================================


====================================================================
1. IDENTIFICAÇÃO DO PROJETO
====================================================================

Nome do projeto:
Trader GPT

Responsável (cliente):
Tiago Rodrigues Vieira

Contato:
tiago.r.vieira@hotmail.com

Stakeholders:
Não possui

Nível de urgência:
Alto


====================================================================
2. OBJETIVO DO PROJETO (VISÃO MACRO)
====================================================================

Criar um sistema de apoio inteligente ao trader discricionário, capaz de analisar uma tela com ferramentas de análise de mercado, apoiar decisões, registrar ações e gerar aprendizado operacional, sem executar ordens automaticamente.

Ferramentas de mercado analisadas visualmente:
- Preço
- Times and Trades
- SuperDOM
- Volume At Price (VAP)
- Gráfico de Candles com VWAP

Decisões possíveis apoiadas pela IA Pré-Trade:
- NEUTRO
- COMPRA
- VENDA

Decisões possíveis apoiadas pela IA com Trade aberto:

- MANTER POSIÇÃO
- COMPRA STOP
- VENDA STOP
- AUMENTAR Posição
- DIMINUIR Posição
- INVERTER

--------------------------------------------------------------------
2.1 Problemas que o sistema resolve
--------------------------------------------------------------------

- Falta de experiência com o mercado e com horários
- Falta de disciplina operacional
- Decisões emocionais e inconsistentes
- Ausência de histórico estruturado
- Dificuldade em avaliar a qualidade das operações


--------------------------------------------------------------------
2.2 Resultados esperados
--------------------------------------------------------------------

- Decisões mais consistentes
- Redução de erros recorrentes
- Separação clara entre decisão humana e apoio da IA
- Base histórica confiável para evolução do trader
- Aumento da assertividade operacional


--------------------------------------------------------------------
2.3 Critérios de sucesso
--------------------------------------------------------------------

- A interface reflete exatamente o que a IA pode ou não pode fazer
- Não existem “mentiras visuais”
- O trader aprende com seus próprios dados
- O sistema aumenta disciplina, não dependência


====================================================================
3. CONTEXTO E MOTIVAÇÃO
====================================================================

O sistema substitui algo existente?
SIM

O que será substituído:
- Anotações manuais
- Prints soltos
- Uso informal de IA sem controle de risco ou estado

Natureza do projeto:
- Interno
- Comercial (potencial futuro)


====================================================================
4. PERFIL DOS USUÁRIOS
====================================================================

Usuário:
Trader

Função:
Operação e decisão

Nível técnico:
Médio


Usuário:
Trader (admin)

Função:
Configuração do sistema

Nível técnico:
Médio / Alto


Usuários simultâneos:
1 (single-user)

Hierarquia de permissões:
Não (neste estágio)


====================================================================
5. FUNCIONALIDADES (REQUISITOS FUNCIONAIS)
====================================================================

--------------------------------------------------------------------
5.1 Funcionalidades obrigatórias
--------------------------------------------------------------------

- Leitura de preço via OCR
- Seleção manual da área da tela para:
  - OCR de preço
  - Captura de tela enviada ao GPT
- Análise pré-trade via IA
- Gestão de posição assistida (análise em trade via IA)
- Análise pós-trade automática (quando habilitada)
- Registro estruturado de:
  - Recomendações pré-trade da IA
  - Recomendações em trade da IA
  - Trades executados pelo usuário
  - Decisões finais do trader
- Controle rigoroso de modos e estados
- Interface com bloqueios coerentes
- Score de disciplina
- Identificação de erros recorrentes
- Comparação decisão IA × decisão trader (eficiência e acertos)
- Aprendizado supervisionado do sistema baseado em:
  - Estatísticas históricas do trader
  - Erros recorrentes identificados
  - Métricas de disciplina


--------------------------------------------------------------------
5.2 Funcionalidades futuras (Roadmap)
--------------------------------------------------------------------

- Persistência de configurações
- Dashboard avançado
- Sugestões de melhoria operacional
- Exportação avançada de dados


====================================================================
6. REGRAS DE NEGÓCIO (LEIS DO SISTEMA)
====================================================================

- O sistema nunca executa ordens automaticamente
- A IA só executa análises se o sistema estiver ligado
- Configurações só podem ser alteradas com o sistema desligado
- Gatilhos automáticos existem apenas no modo automático
- A UI nunca decide lógica, apenas reflete o estado interno
- Em trade aberto:
  - A IA não executa análise automática
  - Apenas uma análise por vez (sem concorrência)

Falhas de OCR ou captura:
- A IA não executa análise
- Estado da IA = BLOQUEADA
- A UI deve exibir erro explícito
- Nenhuma análise ocorre com dados incompletos ou inválidos


--------------------------------------------------------------------
6.1 Sistema de Timer (Regra Global)
--------------------------------------------------------------------

- O sistema possui um Timer Central de Execução
- O Timer:
  - Controla o cooldown entre análises
  - Impede execuções concorrentes
  - É pausado automaticamente:
    - Durante uma análise
    - Durante trade aberto
    - Em modo Observação
- A UI apenas exibe informações do Timer, não controla sua lógica


====================================================================
7. FLUXOS OPERACIONAIS
====================================================================

--------------------------------------------------------------------
Fluxo 1 — Operação Manual
--------------------------------------------------------------------

1. Usuário liga o sistema
2. Seleciona modo Manual
3. Solicita análise da IA
4. Executa trade manualmente
5. Encerra o trade
6. IA executa análise pós-trade
7. Dados são registrados


--------------------------------------------------------------------
Fluxo 2 — Automático Assistido
--------------------------------------------------------------------

1. Usuário configura gatilhos
2. Liga o sistema
3. IA analisa automaticamente
4. Usuário decide se entra no trade
5. Trade é encerrado
6. IA executa análise pós-trade
7. Dados são registrados


--------------------------------------------------------------------
Fluxo 3 — Observação
--------------------------------------------------------------------

1. Sistema ligado em modo Observação
2. Apenas leitura de preço
3. Nenhuma análise da IA é executada
4. Usuário decide entrada
5. Trade é encerrado
6. Dados são registrados


====================================================================
8. INTERFACE E EXPERIÊNCIA (UI/UX)
====================================================================

Design pronto:
Não

Estilo:
Técnico

Plataforma:
Desktop

Princípio UI:
Usuário
  ↓
UI (botão / evento)
  ↓
Engine
  ↓
StateManager / Timer / IA
  ↓
Resultado
  ↓
UI (somente atualização visual)

Estrutura:
ui/
├── app.py              # Janela principal + tabs
├── styles.py           # Cores e estilos semânticos
└── tabs/
    ├── operacao_tab.py
    ├── ia_tab.py
    ├── pos_trade_tab.py
    ├── estatisticas_tab.py
    ├── custos_logs_tab.py
    ├── sistema_tab.py
    └── help_tab.py

====================================================================
9. REQUISITOS TÉCNICOS
====================================================================

Linguagem:
Python

Framework de UI:
Tkinter

Persistência inicial:
CSV

Infraestrutura:
Local

Integrações:
- OpenAI (IA)
- OCR
- Captura de tela


====================================================================
10. SEGURANÇA E CONTROLE
====================================================================

Autenticação:
Login e senha

Controle por nível:
Não

Logs e auditoria:
Sim


====================================================================
11. DADOS E RELATÓRIOS
====================================================================

Dados armazenados:
- Preços
- Trades
- Decisões da IA
- Resultados
- Configurações

Relatórios:
- Performance geral
- Erros recorrentes
- Histórico de decisões

Exportação:
CSV


====================================================================
12. ESTADOS, MODOS E STATUS
====================================================================

Estados do sistema, estados da ia, estados do trade
+------------+-------------------+--------------+-------------------+-----------------------------+-------------+--------------------------------------------+
| SISTEMA    | ESTADO DA IA      | ESTADO TRADE | PODE ANALISAR?    | TIPO DE ANÁLISE             | GATILHO     | OBSERVAÇÕES                                |
+------------+-------------------+--------------+-------------------+-----------------------------+-------------+--------------------------------------------+
| DESLIGADO  | DESLIGADA         | INEXISTENTE  | NÃO               | Nenhuma                     | —           | Sistema inerte                             |
| DESLIGADO  | DESLIGADA         | ABERTO       | NÃO               | Nenhuma                     | —           | Estado inválido (trade não deveria existir)|
| LIGADO     | BLOQUEADA         | INEXISTENTE  | NÃO               | Nenhuma                     | —           | OCR falhou / modo observação               |
| LIGADO     | BLOQUEADA         | ABERTO       | NÃO               | Nenhuma                     | —           | Erro crítico — UI deve alertar             |
| LIGADO     | OCIOSA_MANUAL     | INEXISTENTE  | SIM               | Pré-trade                   | Manual      | Estado padrão do modo Manual               |
| LIGADO     | OCIOSA_AUTOMATICA | INEXISTENTE  | SIM               | Pré-trade                   | Automático  | Respeita cooldown e gatilhos               |
| LIGADO     | ANALISANDO        | INEXISTENTE  | EM EXECUÇÃO       | Pré-trade (em andamento)    | —           | Timer pausado, sistema bloqueado           |
| LIGADO     | GESTAO_POSICAO    | ABERTO       | SIM               | Gestão de posição           | Manual      | Prompt exclusivo de gestão                 |
| LIGADO     | ANALISANDO        | ABERTO       | NÃO               | —                           | —           | Proibido pré-trade com trade aberto        |
| LIGADO     | POS_TRADE         | ENCERRADO    | SIM               | Pós-trade                   | Auto/Manual | Executa uma única vez                      |
| LIGADO     | OCIOSA_MANUAL     | ENCERRADO    | NÃO               | —                           | —           | Aguardando pós-trade                       |
| LIGADO     | OCIOSA_AUTOMATICA | ENCERRADO    | NÃO               | —                           | —           | Pós-trade tem prioridade                   |
+------------+-------------------+--------------+-------------------+-----------------------------+-------------+--------------------------------------------+

Estados do trade, premisses da ia
+------------------+-------------------+---------------------+-------------------+---------------------------------------------+
| ESTADO DO TRADE  | ANÁLISE PRÉ-TRADE | GESTÃO DE POSIÇÃO   | PÓS-TRADE         | OBSERVAÇÕES                                 |
+------------------+-------------------+---------------------+-------------------+---------------------------------------------+
| INEXISTENTE      | SIM               | NÃO                 | NÃO               | Estado normal antes da entrada              |
| ABERTO           | NÃO               | SIM                 | NÃO               | Gestão somente manual                       |
| ENCERRADO        | NÃO               | NÃO                 | SIM               | Pós-trade obrigatório                       |
| ANALISADO        | SIM               | NÃO                 | NÃO               | Retorna ao fluxo normal                     |
+------------------+-------------------+---------------------+-------------------+---------------------------------------------+

Estados da ia, significado operacional
+-------------------+--------------------------------------+------------------------------------+--------------------------------------+
| ESTADO DA IA      | SIGNIFICADO REAL                     | O QUE PODE FAZER                   | O QUE NÃO PODE FAZER                 |
+-------------------+--------------------------------------+------------------------------------+--------------------------------------+
| DESLIGADA         | Sistema desligado                    | Nada                               | Tudo                                 |
| BLOQUEADA         | Erro / observação / dados inválidos  | Exibir erro                        | Qualquer análise                     |
| OCIOSA_MANUAL     | Aguardando ação humana               | Pré-trade manual                  | Analisar sozinha                      |
| OCIOSA_AUTOMATICA | Aguardando gatilhos                  | Pré-trade automático              | Gestão / pós-trade                    |
| ANALISANDO        | Executando pré-trade                 | Leitura de mercado                | Qualquer outra ação                   |
| GESTAO_POSICAO    | Trade aberto                         | Gestão ativa                      | Sugerir entrada                       |
| POS_TRADE         | Trade encerrado                      | Debriefing / avaliação             | Nova análise                         |
+-------------------+--------------------------------------+------------------------------------+--------------------------------------+

Prompts da ia, estado permitido
+----------------------------+------------------------------+----------------------------+
| PROMPT                     | QUANDO PODE RODAR            | ESTADO OBRIGATÓRIO         |
+----------------------------+------------------------------+----------------------------+
| PROMPT_PRE_TRADE           | Sem trade ativo              | IA = ANALISANDO            |
| PROMPT_GESTAO_POSICAO      | Trade ABERTO                 | IA = GESTAO_POSICAO        |
| PROMPT_POS_TRADE           | Trade ENCERRADO              | IA = POS_TRADE             |
+----------------------------+------------------------------+----------------------------+

Modo do Sistema:
- OBSERVAÇÃO  → IA desativada
- MANUAL      → IA sob comando
- AUTOMÁTICO  → IA por gatilhos


====================================================================
13. ABAS DO SISTEMA (RESUMO)
====================================================================

- Operação        → Centro operacional
- IA              → Configuração e risco
- Pós-Trade       → Análise qualitativa
- Estatísticas    → Performance
- Custos & Logs   → Auditoria
- Sistema         → Capturas e resets
- Help            → Educação e segurança


====================================================================
14. PADRÃO DE CORES (SEMÂNTICA GLOBAL)
====================================================================

Verde    → Automático / permitido
Amarelo  → Manual / atenção
Azul     → Gestão / informação
Laranja  → Processando
Vermelho → Bloqueado / risco
Cinza    → Inativo


====================================================================
15. TESTES E VALIDAÇÃO
====================================================================

Testes automatizados:
Não (fase inicial)

Critérios de aceitação:
- Estados corretos
- Bloqueios coerentes
- Nenhuma execução indevida


====================================================================
16. ENTREGA E MANUTENÇÃO
====================================================================

Tipo de entrega:
Código-fonte

Manutenção contínua:
Sim

Documentação:
- Técnica
- Usuário final


====================================================================
17. PRAZOS E RESTRIÇÕES
====================================================================

Prazo:
Evolutivo

Datas críticas:
Não definidas

Orçamento:
—

Restrições legais:
Nenhuma


====================================================================
18. ESTRUTURA DE PASTAS
====================================================================

trader_gpt/
│
├── main.py
│
├── core/
│   ├── state_manager.py
│   ├── timer.py
│   ├── modes.py
│   └── engine.py
│
├── ui/
│   ├── app.py
│   ├── styles.py
│   └── tabs/
│       ├── operacao_tab.py
│       ├── ia_tab.py
│       ├── pos_trade_tab.py
│       ├── estatisticas_tab.py
│       ├── custos_logs_tab.py
│       ├── sistema_tab.py
│       └── help_tab.py
│
├── ia/
│   ├── prompts.py
│   ├── analyzer_pre_trade.py
│   ├── analyzer_gestao.py
│   ├── analyzer_pos_trade.py
│   └── decision_parser.py
│
├── ocr/
│   ├── screen_selector.py
│   ├── price_reader.py
│   └── ocr_engine.py
│
├── capture/
│   ├── screen_capture.py
│   └── capture_test.py
│
├── data/
│   ├── models.py
│   ├── repositories.py
│   └── serializers.py
│
├── logs/
│   ├── data/
│   │   ├── prices.csv
│   │   ├── trades.csv
│   │   ├── ia_decisions.csv
│   │   └── pos_trade.csv
│   └── system.log
│
├── stats/
│   ├── metrics.py
│   ├── discipline_score.py
│   └── error_patterns.py
│
├── config/
│   ├── defaults.py
│   └── runtime_config.py
│
├── utils/
│   ├── time_utils.py
│   ├── file_utils.py
│   └── validators.py
│
└── README.md


====================================================================
19. PROMPTS DO SISTEMA TRADER GPT
====================================================================

[INCLUÍDOS INTEGRALMENTE — PRÉ-TRADE, GESTÃO DE POSIÇÃO E PÓS-TRADE,
SEM QUALQUER ALTERAÇÃO DE CONTEÚDO]

# -*- coding: utf-8 -*-
"""
Arquivo: prompts.py
Projeto: Trader GPT
Função: Contratos de linguagem da IA (PROMPTS CANÔNICOS)

⚠️ ATENÇÃO:
Este arquivo define os LIMITES OPERACIONAIS da IA.
Qualquer alteração aqui impacta diretamente:
- Risco operacional
- Disciplina do trader
- Coerência entre UI, engine e IA

Versão dos prompts: v1.0
Congelado em: 2026-01
"""

# =====================================================
# PROMPTS DO SISTEMA TRADER GPT
# =====================================================


# =====================================================
# 1. PROMPT — ANÁLISE PRÉ-TRADE (LEITURA DE MERCADO)
# =====================================================

PROMPT_PRE_TRADE_WIN = """
Você é um analista profissional do mercado futuro brasileiro (WIN), especializado em:

- Scalp de Fluxo (Tape Reading) — ESTRATÉGIA PRINCIPAL
- VWAP + Delta (Fluxo Institucional)
- Scalp de Pullback (com fluxo)
- Price Action + Fluxo (fluxo sempre confirma)

Seu papel é analisar INTENÇÃO, DOMINÂNCIA e PROBABILIDADE.
Você NÃO prevê mercado e NÃO inventa informações.

----------------------------------------------------------------
A imagem fornecida contém APENAS:
- Gráfico de candles (1 min)
- VWAP
- VAP (Volume At Price / Volume Profile)
- Times & Trades
- SuperDOM

Contexto adicional fornecido pelo sistema:
- Preço atual: {preco_atual}
- Estatísticas do trader: {resumo_stats}

Analise SOMENTE o que está VISÍVEL na imagem.
Se algo não estiver claro, legível ou presente, assuma NEUTRO (INDEFINIÇÃO OPERACIONAL)

----------------------------------------------------------------
HIERARQUIA OBRIGATÓRIA DE DECISÃO
Avalie SEMPRE nesta ordem:

1. Scalp de Fluxo (Tape Reading)
2. VWAP + Delta (Institucional)
3. Scalp de Pullback (com fluxo)
4. Price Action + Fluxo (apenas confirmação)

----------------------------------------------------------------
CRITÉRIOS OBJETIVOS POR ESTRATÉGIA

1) SCALP DE FLUXO (TAPE READING) — PRIORIDADE MÁXIMA
Avalie:
- Sequência e intensidade das agressões no Times & Trades
- Defesa e absorção visível no SuperDOM
- Repetição de negócios no mesmo preço
- Falha de continuação contra o fluxo dominante

Decisão:
- COMPRA: compradores agridem, vendedores são absorvidos, preço não cede
- VENDA: vendedores agridem, compradores são absorvidos, preço não reage
- NEUTRO: agressões alternadas, absorção dupla ou fluxo lento

Ignore candles bonitos sem confirmação de fluxo.

----------------------------------------------------------------
2) VWAP + DELTA (INSTITUCIONAL)
Avalie:
- Preço acima, abaixo ou testando a VWAP
- Rejeição ou aceitação da VWAP
- Fluxo confirmando a reação
- Absorção institucional na VWAP ou desvios

Decisão:
- COMPRA: rejeição da VWAP com fluxo comprador dominante
- VENDA: rejeição da VWAP com fluxo vendedor dominante
- NEUTRO: preço cruzando a VWAP sem reação clara

VWAP sem fluxo NÃO gera trade.

----------------------------------------------------------------
3) SCALP DE PULLBACK (COM FLUXO)
Avalie:
- Tendência clara no gráfico
- Pullback contra a tendência
- Redução de agressão no pullback
- Absorção no final da correção
- Retomada do fluxo a favor da tendência

Decisão:
- COMPRA: tendência de alta + pullback controlado + retomada compradora
- VENDA: tendência de baixa + pullback controlado + retomada vendedora
- NEUTRO: correção profunda, congestão ou inversão de fluxo

Nunca opere pullback contra a microtendência.

----------------------------------------------------------------
4) PRICE ACTION + FLUXO (CONFIRMAÇÃO)
Avalie:
- Estrutura de topos e fundos
- Suporte, resistência, VWAP, POC, HVN, LVN
- Falha de rompimento ou candle de rejeição
- Confirmação clara no fluxo

Price Action sem fluxo é INVALIDO.

----------------------------------------------------------------
CONDIÇÕES AUTOMÁTICAS DE NEUTRO
Retorne NEUTRO se identificar:
- Mercado lateral ou congestionado
- Fluxo simétrico
- Absorção dos dois lados
- Spikes erráticos ou abertura desorganizada
- Stop técnico indefinido

----------------------------------------------------------------
CRITÉRIO PARA O CAMPO "CONFIANÇA":

- 80–100: Fluxo dominante claro, absorção visível, sem conflito entre ferramentas
- 60–79: Fluxo predominante, mas com algum ruído ou contexto neutro
- 40–59: Leve dominância, estrutura incompleta ou confirmação parcial
- 0–39: Mercado confuso, lateral ou indefinido (normalmente NEUTRO)

----------------------------------------------------------------
FORMATO DE RESPOSTA (OBRIGATÓRIO)

Retorne APENAS no formato abaixo:

Viés: COMPRA | VENDA | NEUTRO
Confiança: 0-100

JUSTIFICATIVA:
Times & Trades:
SuperDOM:
Gráfico (candlestick):
VWAP:
Volume At Price:
Fluxo dominante (macro / micro):
Absorção observada:
Relação com VWAP / VAP:
Estrutura de preço:

----------------------------------------------------------------
REGRAS FINAIS (IMUTÁVEIS)
- Nunca invente dados
- Fluxo decide, Price Action organiza, VWAP contextualiza
- Se o Viés for NEUTRO, a justificativa deve deixar claro a AUSÊNCIA de edge
- Não tente “forçar” leitura quando o mercado estiver indefinido
"""


# =====================================================
# 2. PROMPT — GESTÃO DE POSIÇÃO
# =====================================================

PROMPT_GESTAO_POSICAO_WIN = """
Você é um mentor profissional de trading, especialista em:
- Tape Reading (Fluxo)
- Gestão ativa de posição no mercado futuro (WIN)
- Execução profissional e controle de risco

Seu papel é **AUXILIAR NA GESTÃO DA POSIÇÃO JÁ ABERTA**.

Gestão de posição, neste contexto, significa decidir entre:
- REALIZAR NOVA OPERAÇÃO NO MESMO SENTIDO (AUMENTAR POSIÇÃO)
- PERMANECER (AGUARDAR / NÃO FAZER NADA)
- REDUZIR (REALIZAR PARCIAL)
- ZERAR A POSIÇÃO
- INVERTER A POSIÇÃO

Você NÃO cria setups novos.
Você NÃO prevê mercado.
Você NÃO força operações.
Você analisa SOMENTE o que está visível na imagem.

------------------------------------------------------------
CONTEXTO DA OPERAÇÃO (POSIÇÃO JÁ ABERTA):

- Tipo da posição atual: {tipo_operacao}  (COMPRA ou VENDA)
- Preço médio de entrada: {preco_entrada}
- Preço atual: {preco_atual}
- Resultado atual (pontos): {pnl_atual}

------------------------------------------------------------
CONTEXTO DE ANÁLISE (IMAGEM):

A imagem fornecida contém:
- Gráfico de candles (1 minuto)
- VWAP
- Volume At Price (VAP / Volume Profile)
- Times & Trades
- SuperDOM

Analise SOMENTE o que está VISÍVEL.
Se algo não estiver claro ou legível, declare explicitamente.

------------------------------------------------------------
HIERARQUIA OBRIGATÓRIA DE ANÁLISE (NESTA ORDEM):

1. FLUXO (PRIORIDADE MÁXIMA)
2. CONTEXTO DE PREÇO
3. ESTRUTURA E COMPORTAMENTO

------------------------------------------------------------
FORMATO DE RESPOSTA (OBRIGATÓRIO):

GESTÃO DA POSIÇÃO:
AUMENTAR | PERMANECER | REDUZIR | ZERAR | INVERTER

CONFIANÇA: 0–100

JUSTIFICATIVA:
Fluxo:
VWAP / VAP:
Estrutura de preço:
Risco atual:

AÇÃO SUGERIDA:
(1 ação prática, clara e executável agora)
"""


# =====================================================
# 3. PROMPT — ANÁLISE PÓS-TRADE
# =====================================================

PROMPT_POS_TRADE_WIN = """
Você é um mentor profissional de trading, especialista em:
- Tape Reading (Fluxo)
- Price Action aplicado ao WIN
- Disciplina operacional e execução técnica

Analise um trade JÁ ENCERRADO.
Seu papel é avaliar o PROCESSO, a DISCIPLINA e a COERÊNCIA com a análise pré-trade.

Você NÃO julga emocionalmente e NÃO relativiza erro técnico.

----------------------------------------------------------------
(Conteúdo integral mantido conforme versão original)
----------------------------------------------------------------
"""

====================================================================
20. CONFIRMAÇÃO
====================================================================

Ao enviar este documento, o cliente confirma que:

- As informações refletem sua necessidade real
- Mudanças futuras podem impactar prazo e custo
- O projeto será validado por etapas

Assinatura:
Tiago Rodrigues Vieira

Data:
___ / ___ / _____


====================================================================
FIM DO DOCUMENTO
====================================================================