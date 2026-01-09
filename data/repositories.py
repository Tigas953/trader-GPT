# data/repositories.py

import csv
import os
from pathlib import Path
from typing import Any

from data.models import Trade, PreTradeAnalysis


# =====================================================
# CONFIGURAÇÃO BASE
# =====================================================

BASE_LOG_PATH = Path("logs/data")


# =====================================================
# REPOSITÓRIO BASE (CSV — APPEND ONLY)
# =====================================================

class BaseCSVRepository:
    """
    Repositório base para escrita em CSV.
    - Escrita somente em modo append
    - Header garantido
    - Validação de campos obrigatórios
    """

    def __init__(self, filename: str, fieldnames: list[str]):
        self.filepath = BASE_LOG_PATH / filename
        self.fieldnames = fieldnames
        self._ensure_file()

    def _ensure_file(self) -> None:
        os.makedirs(self.filepath.parent, exist_ok=True)

        if not self.filepath.exists():
            with open(self.filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writeheader()

    def append(self, data: dict[str, Any]) -> None:
        self._validate(data)

        with open(self.filepath, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(data)

    def _validate(self, data: dict[str, Any]) -> None:
        missing_fields = set(self.fieldnames) - set(data.keys())

        if missing_fields:
            raise ValueError(
                f"Campos ausentes no registro CSV: {missing_fields}"
            )


# =====================================================
# REPOSITÓRIO DE TRADES
# =====================================================

class TradeRepository(BaseCSVRepository):
    """
    Persistência de trades executados pelo trader.
    """

    def __init__(self):
        super().__init__(
            filename="trades.csv",
            fieldnames=[
                "trade_id",
                "tipo",
                "preco_entrada",
                "preco_saida",
                "pnl",
                "timestamp_abertura",
                "timestamp_fechamento",
            ],
        )

    def save(self, trade: Trade) -> None:
        if not isinstance(trade, Trade):
            raise TypeError("Objeto inválido para TradeRepository")

        self.append(trade.to_dict())


# =====================================================
# REPOSITÓRIO DE ANÁLISE PRÉ-TRADE
# =====================================================

class PreTradeRepository(BaseCSVRepository):
    """
    Persistência das análises pré-trade geradas pela IA.
    """

    def __init__(self):
        super().__init__(
            filename="ia_decisions.csv",
            fieldnames=[
                "analysis_id",
                "vies",
                "confianca",
                "justificativa",
                "preco_atual",
                "timestamp",
            ],
        )

    def save(self, analysis: PreTradeAnalysis) -> None:
        if not isinstance(analysis, PreTradeAnalysis):
            raise TypeError("Objeto inválido para PreTradeRepository")

        self.append(analysis.to_dict())
