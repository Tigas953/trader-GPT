from dataclasses import dataclass
from typing import Literal


# =====================================================
# EXCEÇÃO DE PARSE
# =====================================================

class InvalidIAResponse(Exception):
    """Resposta da IA inválida ou fora do contrato esperado."""
    pass


# =====================================================
# MODELOS DE DECISÃO (CONTRATO IMUTÁVEL)
# =====================================================

@dataclass(frozen=True)
class PreTradeDecision:
    vies: Literal["COMPRA", "VENDA", "NEUTRO"]
    confianca: int
    justificativa: str


@dataclass(frozen=True)
class GestaoDecision:
    acao: Literal["AUMENTAR", "PERMANECER", "REDUZIR", "ZERAR", "INVERTER"]
    confianca: int
    justificativa: str


@dataclass(frozen=True)
class PosTradeDecision:
    avaliacao: Literal["BOM", "RUIM", "NEUTRO"]
    score_disciplina: int
    alinhamento_gpt: Literal["SIM", "NÃO", "PARCIAL"]
    erro_identificado: str
    erro_recorrente: bool
    diagnostico: str
    sugestao: str


# =====================================================
# PARSER CENTRAL
# =====================================================

class DecisionParser:
    """
    Parser responsável por validar e estruturar respostas da IA.
    Aceita apenas dicts EXATAMENTE no formato esperado.
    """

    # -------------------------------
    # Helpers
    # -------------------------------

    @staticmethod
    def _validate_confidence(value: int):
        if not isinstance(value, int) or not (0 <= value <= 100):
            raise InvalidIAResponse("Confiança fora do intervalo 0–100")

    @staticmethod
    def _validate_text(value: str, field: str, min_len: int = 5):
        if not isinstance(value, str):
            raise InvalidIAResponse(f"{field} deve ser string")
        if len(value.strip()) < min_len:
            raise InvalidIAResponse(f"{field} muito curto ou vazio")

    # -------------------------------
    # PRE-TRADE
    # -------------------------------

    @staticmethod
    def parse_pre_trade(response: dict) -> PreTradeDecision:
        required = {"vies", "confianca", "justificativa"}
        if set(response.keys()) != required:
            raise InvalidIAResponse("Estrutura inválida no pré-trade")

        vies = response["vies"]
        confianca = int(response["confianca"])
        justificativa = response["justificativa"]

        if vies not in {"COMPRA", "VENDA", "NEUTRO"}:
            raise InvalidIAResponse("Viés inválido")

        DecisionParser._validate_confidence(confianca)
        DecisionParser._validate_text(justificativa, "Justificativa")

        return PreTradeDecision(
            vies=vies,
            confianca=confianca,
            justificativa=justificativa.strip(),
        )

    # -------------------------------
    # GESTÃO DE POSIÇÃO
    # -------------------------------

    @staticmethod
    def parse_gestao(response: dict) -> GestaoDecision:
        required = {"acao", "confianca", "justificativa"}
        if set(response.keys()) != required:
            raise InvalidIAResponse("Estrutura inválida na gestão")

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
        DecisionParser._validate_text(justificativa, "Justificativa")

        return GestaoDecision(
            acao=acao,
            confianca=confianca,
            justificativa=justificativa.strip(),
        )

    # -------------------------------
    # PÓS-TRADE
    # -------------------------------

    @staticmethod
    def parse_pos_trade(response: dict) -> PosTradeDecision:
        required = {
            "avaliacao",
            "score_disciplina",
            "alinhamento_gpt",
            "erro_identificado",
            "erro_recorrente",
            "diagnostico",
            "sugestao",
        }
        if set(response.keys()) != required:
            raise InvalidIAResponse("Estrutura inválida no pós-trade")

        avaliacao = response["avaliacao"]
        score = int(response["score_disciplina"])
        alinhamento = response["alinhamento_gpt"]
        erro = response["erro_identificado"]
        erro_recorrente = response["erro_recorrente"]
        diagnostico = response["diagnostico"]
        sugestao = response["sugestao"]

        if avaliacao not in {"BOM", "RUIM", "NEUTRO"}:
            raise InvalidIAResponse("Avaliação inválida")

        if alinhamento not in {"SIM", "NÃO", "PARCIAL"}:
            raise InvalidIAResponse("Alinhamento GPT inválido")

        if not isinstance(erro_recorrente, bool):
            raise InvalidIAResponse("Erro recorrente deve ser boolean")

        DecisionParser._validate_confidence(score)
        DecisionParser._validate_text(erro, "Erro identificado")
        DecisionParser._validate_text(diagnostico, "Diagnóstico")
        DecisionParser._validate_text(sugestao, "Sugestão")

        return PosTradeDecision(
            avaliacao=avaliacao,
            score_disciplina=score,
            alinhamento_gpt=alinhamento,
            erro_identificado=erro.strip(),
            erro_recorrente=erro_recorrente,
            diagnostico=diagnostico.strip(),
            sugestao=sugestao.strip(),
        )
