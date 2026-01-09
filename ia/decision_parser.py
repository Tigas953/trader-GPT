# ia/decision_parser.py

from dataclasses import dataclass
from typing import Optional


# =====================================================
# EXCEÇÃO DE PARSE
# =====================================================

class InvalidIAResponse(Exception):
    """Resposta da IA inválida ou fora do contrato esperado."""
    pass


# =====================================================
# MODELOS DE DECISÃO
# =====================================================

@dataclass(frozen=True)
class PreTradeDecision:
    vies: str               # COMPRA | VENDA | NEUTRO
    confianca: int          # 0-100
    justificativa: str


@dataclass(frozen=True)
class GestaoDecision:
    acao: str               # AUMENTAR | PERMANECER | REDUZIR | ZERAR | INVERTER
    confianca: int
    justificativa: str


@dataclass(frozen=True)
class PosTradeDecision:
    avaliacao: str          # BOM | RUIM | NEUTRO
    score_disciplina: int   # 0-100
    erro_identificado: str
    sugestao: str


# =====================================================
# PARSER CENTRAL
# =====================================================

class DecisionParser:
    """
    Parser responsável por validar e estruturar respostas da IA.
    """

    @staticmethod
    def _validate_confidence(value: int):
        if not isinstance(value, int) or not (0 <= value <= 100):
            raise InvalidIAResponse("Confiança fora do intervalo 0–100")

    @staticmethod
    def parse_pre_trade(response: dict) -> PreTradeDecision:
        try:
            vies = response["vies"]
            confianca = int(response["confianca"])
            justificativa = response["justificativa"]

            if vies not in {"COMPRA", "VENDA", "NEUTRO"}:
                raise InvalidIAResponse("Viés inválido")

            DecisionParser._validate_confidence(confianca)

            return PreTradeDecision(
                vies=vies,
                confianca=confianca,
                justificativa=justificativa.strip(),
            )

        except KeyError as e:
            raise InvalidIAResponse(f"Campo ausente: {e}")

    @staticmethod
    def parse_gestao(response: dict) -> GestaoDecision:
        try:
            acao = response["acao"]
            confianca = int(response["confianca"])
            justificativa = response["justificativa"]

            if acao not in {
                "AUMENTAR",
                "PERMANECER",
                "REDUZIR",
                "ZERAR",
                "INVERTER",
            }:
                raise InvalidIAResponse("Ação de gestão inválida")

            DecisionParser._validate_confidence(confianca)

            return GestaoDecision(
                acao=acao,
                confianca=confianca,
                justificativa=justificativa.strip(),
            )

        except KeyError as e:
            raise InvalidIAResponse(f"Campo ausente: {e}")

    @staticmethod
    def parse_pos_trade(response: dict) -> PosTradeDecision:
        try:
            avaliacao = response["avaliacao"]
            score = int(response["score_disciplina"])
            erro = response["erro_identificado"]
            sugestao = response["sugestao"]

            if avaliacao not in {"BOM", "RUIM", "NEUTRO"}:
                raise InvalidIAResponse("Avaliação inválida")

            DecisionParser._validate_confidence(score)

            return PosTradeDecision(
                avaliacao=avaliacao,
                score_disciplina=score,
                erro_identificado=erro.strip(),
                sugestao=sugestao.strip(),
            )

        except KeyError as e:
            raise InvalidIAResponse(f"Campo ausente: {e}")
