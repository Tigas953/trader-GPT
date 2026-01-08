# data/repositories.py

import csv
import os
from datetime import datetime
from typing import Any
from pathlib import Path


BASE_LOG_PATH = Path("logs/data")


class CSVRepository:
    """
    Repositório base para escrita em CSV (append-only).
    """

    def __init__(self, filename: str, fieldnames: list[str]):
        self.filepath = BASE_LOG_PATH / filename
        self.fieldnames = fieldnames
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(self.filepath.parent, exist_ok=True)
        if not self.filepath.exists():
            with open(self.filepath, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    def append(self, data: dict[str, Any]):
        self._validate(data)
        with open(self.filepath, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(data)

    def _validate(self, data: dict[str, Any]):
        missing = set(self.fieldnames) - set(data.keys())
        if missing:
            raise ValueError(f"Campos ausentes no registro: {missing}")


# =====================================================
# REPOSITÓRIOS CONCRETOS
# =====================================================

trade_repo = CSVRepository(
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

pre_trade_repo = CSVRepository(
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

gestao_repo = CSVRepository(
    filename="ia_gestao.csv",
    fieldnames=[
        "trade_id",
        "decisao",
        "confianca",
        "justificativa",
        "pnl_momento",
        "timestamp",
    ],
)

pos_trade_repo = CSVRepository(
    filename="pos_trade.csv",
    fieldnames=[
        "trade_id",
        "avaliacao",
        "score_disciplina",
        "alinhamento_gpt",
        "erro_identificado",
        "erro_recorrente",
        "diagnostico",
        "sugestao",
        "timestamp",
    ],
)
