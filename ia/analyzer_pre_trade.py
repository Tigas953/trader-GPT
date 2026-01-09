# ia/analyzer_pre_trade.py

from typing import Dict, Any

from ia.prompts import PROMPT_PRE_TRADE_WIN
from ia.decision_parser import DecisionParser, PreTradeDecision
from ia.decision_parser import InvalidIAResponse


class PreTradeAnalyzer:
    """
    Executor de análise pré-trade.
    Recebe contexto válido, chama IA e retorna decisão estruturada.
    """

    def __init__(self, llm_client):
        """
        llm_client deve ser um cliente já configurado (OpenAI ou similar),
        com método: generate(prompt: str) -> str
        """
        self._llm = llm_client

    def run(
        self,
        image_description: str,
        preco_atual: float,
        resumo_stats: str,
    ) -> PreTradeDecision:
        """
        Executa a análise pré-trade.

        Retorna:
            PreTradeDecision (objeto validado)

        Lança:
            InvalidIAResponse se a resposta for inválida
        """

        prompt = PROMPT_PRE_TRADE_WIN.format(
            preco_atual=preco_atual,
            resumo_stats=resumo_stats,
        )

        raw_response = self._llm.generate(prompt)

        response_dict = self._parse_raw_response(raw_response)

        return DecisionParser.parse_pre_trade(response_dict)

    # =====================================================
    # MÉTODOS INTERNOS
    # =====================================================

    def _parse_raw_response(self, text: str) -> Dict[str, Any]:
        """
        Converte texto bruto da IA em dicionário.
        Espera formato rígido definido no prompt.
        """

        try:
            lines = [line.strip() for line in text.splitlines() if line.strip()]

            data = {}

            for line in lines:
                if ":" not in line:
                    continue

                key, value = line.split(":", 1)
                data[key.strip().lower()] = value.strip()

            mapped = {
                "vies": data.get("viés") or data.get("vies"),
                "confianca": data.get("confiança") or data.get("confianca"),
                "justificativa": text,
            }

            return mapped

        except Exception as exc:
            raise InvalidIAResponse(f"Falha ao interpretar resposta da IA: {exc}")
