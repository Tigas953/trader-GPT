# data/models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# =====================================================
# MODELO: TRADE
# =====================================================

@dataclass(frozen=True)
class Trade:
    trade_id: str
    tipo: str                 # COMPRA | VENDA
    preco_entrada: float
    preco_saida: Optional[float]
    pnl: Optional[float]
    timestamp_abertura: datetime
    timestamp_fechamento: Optional[datetime]


# =====================================================
# MODELO: ANÁLISE PRÉ-TRADE
# =====================================================

@dataclass(frozen=True)
class AnalisePreTrade:
    analysis_id: str
    vies: str                 # COMPRA | VENDA | NEUTRO
    confianca: int             # 0–100
    justificativa: str
    preco_atual: float
    timestamp: datetime


# =====================================================
# MODELO: GESTÃO DE POSIÇÃO
# =====================================================

@dataclass(frozen=True)
class GestaoPosicao:
    trade_id: str
    decisao: str               # AUMENTAR | PERMANECER | REDUZIR | ZERAR | INVERTER
    confianca: int             # 0–100
    justificativa: str
    pnl_momento: float
    timestamp: datetime


# =====================================================
# MODELO: PÓS-TRADE
# =====================================================

@dataclass(frozen=True)
class PosTrade:
    trade_id: str
    avaliacao: str             # BOM | RUIM | NEUTRO
    score_disciplina: int      # 0–100
    alinhamento_gpt: str       # SIM | NÃO | PARCIAL
    erro_identificado: str
    erro_recorrente: bool
    diagnostico: str
    sugestao: str
    timestamp: datetime
