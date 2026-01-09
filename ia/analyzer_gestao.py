# ia/analyzer_gestao.py

from typing import Dict, Any

from ia.prompts import PROMPT_GESTAO_POSICAO_WIN
from ia.decision_parser import DecisionParser, GestaoDecision
from ia.decision_parser import InvalidIAResponse


class GestaoPositionAnalyzer:
    """
    Executor de análise de gestão de posição.
    Atua SOMENTE com trade já aberto.
    """

    def __init__(self, llm_client):
        """
        llm_client deve expor:
        generate(prompt: str) -> str
        """
        self._llm = llm_client

    def run(
        self,
        tipo_operacao: str,
        preco_entrada: float,
        preco_atual: float,
        pnl_atual: float,
    ) -> GestaoDecision:
        """
        Executa a análise de gestão da posição.

        Retorna:
            GestaoDecision (objeto validado)

        Lança:
            InvalidIAResponse se resposta for inválida
        """

        prompt = PROMPT_GESTAO_POSICAO_WIN.format(
            tipo_operacao=tipo_operacao,
            preco_entrada=preco_entrada,
            preco_atual=preco_atual,
            pnl_atual=pnl_atual,
        )

        raw_response = self._llm.generate(prompt)

        parsed = self._parse_raw_response(raw_response)

        return DecisionParser.parse_gestao(parsed)

    # =====================================================
    # MÉTODOS INTERNOS
    # =====================================================

    def _parse_raw_response(self, text: str) -> Dict[str, Any]:
        """
        Converte texto da IA em estrutura intermediária.
        Mantém o texto bruto como justificativa.
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
                "decisao": data.get("gestão da posição") or data.get("gestao da posicao"),
                "confianca": data.get("confiança") or data.get("confianca"),
                "justificativa": text,
            }

            return mapped

        except Exception as exc:
            raise InvalidIAResponse(
                f"Erro ao interpretar resposta da IA (gestão): {exc}"
            )
