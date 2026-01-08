# ia/analyzer_pre_trade.py

from ia.prompts import PROMPT_PRE_TRADE_WIN
from ia.decision_parser import parse_decision, IADecision


def run_pre_trade_analysis(
    image_path: str,
    preco_atual: float,
    resumo_stats: str,
    llm_client
) -> IADecision:
    """
    Executa análise pré-trade.
    """
    prompt = PROMPT_PRE_TRADE_WIN.format(
        preco_atual=preco_atual,
        resumo_stats=resumo_stats
    )

    response = llm_client.run(prompt=prompt, image=image_path)

    if not response:
        raise RuntimeError("IA não retornou resposta")

    return parse_decision(response)
