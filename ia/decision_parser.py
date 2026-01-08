# ia/decision_parser.py

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class IADecision:
    action: str
    confidence: int
    raw_text: str


VALID_ACTIONS = {
    "COMPRA",
    "VENDA",
    "NEUTRO",
    "AUMENTAR",
    "PERMANECER",
    "REDUZIR",
    "ZERAR",
    "INVERTER",
    "BOM",
    "RUIM",
    "NEUTRO",
}


def parse_decision(text: str) -> IADecision:
    """
    Valida e extrai decisão da resposta da IA.
    """
    action_match = re.search(r"(COMPRA|VENDA|NEUTRO|AUMENTAR|PERMANECER|REDUZIR|ZERAR|INVERTER|BOM|RUIM)", text)
    confidence_match = re.search(r"(\d{1,3})", text)

    if not action_match:
        raise ValueError("Resposta IA sem ação válida")

    action = action_match.group(1)

    if action not in VALID_ACTIONS:
        raise ValueError("Ação IA fora do conjunto permitido")

    confidence = None
    if confidence_match:
        confidence = int(confidence_match.group(1))
        if confidence < 0 or confidence > 100:
            raise ValueError("Confiança fora do intervalo 0–100")

    return IADecision(
        action=action,
        confidence=confidence if confidence is not None else 0,
        raw_text=text
    )
