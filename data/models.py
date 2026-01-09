# data/models.py

from datetime import datetime
from typing import Optional


# =====================================================
# EXCEÇÃO DE DADOS INVÁLIDOS
# =====================================================

class InvalidDataError(Exception):
    """Erro lançado quando um modelo recebe dados inválidos."""
    pass


# =====================================================
# BASE MODEL (UTILITÁRIO)
# =====================================================

class BaseModel:
    def _validate_not_none(self, field_name, value):
        if value is None:
            raise InvalidDataError(f"Campo obrigatório ausente: {field_name}")

    def _validate_type(self, field_name, value, expected_type):
        if not isinstance(value, expected_type):
            raise InvalidDataError(
                f"Campo '{field_name}' deve ser do tipo {expected_type.__name__}"
            )


# =====================================================
# MODELO: TRADE
# =====================================================

class Trade(BaseModel):
    def __init__(
        self,
        trade_id: str,
        side: str,  # COMPRA ou VENDA
        entry_price: float,
        exit_price: Optional[float],
        pnl: Optional[float],
        opened_at: datetime,
        closed_at: Optional[datetime],
    ):
        self._validate_not_none("trade_id", trade_id)
        self._validate_not_none("side", side)
        self._validate_type("entry_price", entry_price, (int, float))
        self._validate_type("opened_at", opened_at, datetime)

        if side not in {"COMPRA", "VENDA"}:
            raise InvalidDataError("side deve ser COMPRA ou VENDA")

        self.trade_id = trade_id
        self.side = side
        self.entry_price = float(entry_price)
        self.exit_price = float(exit_price) if exit_price is not None else None
        self.pnl = float(pnl) if pnl is not None else None
        self.opened_at = opened_at
        self.closed_at = closed_at

    def is_closed(self) -> bool:
        return self.exit_price is not None


# =====================================================
# MODELO: ANÁLISE PRÉ-TRADE
# =====================================================

class PreTradeAnalysis(BaseModel):
    def __init__(
        self,
        trade_id: str,
        bias: str,  # COMPRA | VENDA | NEUTRO
        confidence: int,  # 0–100
        justification: str,
        created_at: datetime,
    ):
        self._validate_not_none("trade_id", trade_id)
        self._validate_not_none("bias", bias)
        self._validate_type("confidence", confidence, int)

        if bias not in {"COMPRA", "VENDA", "NEUTRO"}:
            raise InvalidDataError("bias inválido")

        if not 0 <= confidence <= 100:
            raise InvalidDataError("confidence deve estar entre 0 e 100")

        self.trade_id = trade_id
        self.bias = bias
        self.confidence = confidence
        self.justification = justification
        self.created_at = created_at


# =====================================================
# MODELO: GESTÃO DE POSIÇÃO
# =====================================================

class PositionManagement(BaseModel):
    def __init__(
        self,
        trade_id: str,
        action: str,  # AUMENTAR | PERMANECER | REDUZIR | ZERAR | INVERTER
        confidence: int,
        note: str,
        created_at: datetime,
    ):
        self._validate_not_none("trade_id", trade_id)

        if action not in {
            "AUMENTAR",
            "PERMANECER",
            "REDUZIR",
            "ZERAR",
            "INVERTER",
        }:
            raise InvalidDataError("Ação de gestão inválida")

        if not 0 <= confidence <= 100:
            raise InvalidDataError("confidence inválido")

        self.trade_id = trade_id
        self.action = action
        self.confidence = confidence
        self.note = note
        self.created_at = created_at


# =====================================================
# MODELO: PÓS-TRADE
# =====================================================

class PostTradeAnalysis(BaseModel):
    def __init__(
        self,
        trade_id: str,
        evaluation: str,  # BOM | RUIM | NEUTRO
        discipline_score: int,  # 0–100
        error: str,
        recurring_error: bool,
        diagnosis: str,
        suggestion: str,
        created_at: datetime,
    ):
        if evaluation not in {"BOM", "RUIM", "NEUTRO"}:
            raise InvalidDataError("evaluation inválido")

        if not 0 <= discipline_score <= 100:
            raise InvalidDataError("discipline_score inválido")

        self.trade_id = trade_id
        self.evaluation = evaluation
        self.discipline_score = discipline_score
        self.error = error
        self.recurring_error = recurring_error
        self.diagnosis = diagnosis
        self.suggestion = suggestion
        self.created_at = created_at
