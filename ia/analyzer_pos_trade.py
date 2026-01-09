# ia/analyzer_pos_trade.py

from typing import Dict, Any

from ia.prompts import PROMPT_POS_TRADE_WIN
from ia.decision_parser import DecisionParser, PosTradeDecision
from ia.decision_parser import InvalidIAResponse


class PosTradeAnalyzer:
    """
    Executor de análise pós-trade.
    Atua SOMENTE com trade ENCERRADO.
    """

    def __init__(self, llm_client):
        """
        llm_client deve expor:
        generate(prompt: str) -> str
        """
        self._llm = llm_client

    def run(
        self,
        tipo: str,
        preco_entrada: float,
        preco_saida: float,
        pnl: float,
        vies_gpt: str,
        confianca_gpt: int,
        erros_recorrentes: str,
        disciplina_media: int,
    ) -> PosTradeDecision:
        """
        Executa a análise pós-trade.

        Retorna:
            PosTradeDecision (objeto validado)

        Lança:
            InvalidIAResponse se resposta for inválida
        """

        prompt = PROMPT_POS_TRADE_WIN.format(
            tipo=tipo,
            preco_entrada=preco_entrada,
            preco_saida=preco_saida,
            pnl=pnl,
            vies_gpt=vies_gpt,
            confianca_gpt=confianca_gpt,
            erros_recorrentes=erros_recorrentes or "DADO NÃO DISPONÍVEL",
            disciplina_media=disciplina_media or "DADO NÃO DISPONÍVEL",
        )

        raw_response = self._llm.generate(prompt)

        parsed = self._parse_raw_response(raw_response)

        return DecisionParser.parse_pos_trade(parsed)

    # =====================================================
    # MÉTODOS INTERNOS
    # =====================================================

    def _parse_raw_response(self, text: str) -> Dict[str, Any]:
        """
        Converte texto da IA em estrutura intermediária.
        Mantém o texto bruto para auditoria.
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
                "avaliacao": data.get("avaliação") or data.get("avaliacao"),
                "score_disciplina": data.get("score"),
                "alinhamento_gpt": data.get("alinhamento com gpt"),
                "erro_identificado": data.get("erro identificado"),
                "erro_recorrente": data.get("erro recorrente"),
                "diagnostico": data.get("diagnóstico") or data.get("diagnostico"),
                "sugestao": data.get("sugestão") or data.get("sugestao"),
                "raw_text": text,
            }

            return mapped

        except Exception as exc:
            raise InvalidIAResponse(
                f"Erro ao interpretar resposta da IA (pós-trade): {exc}"
            )
