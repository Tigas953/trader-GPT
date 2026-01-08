# ia/analyzer_pos_trade.py

from ia.prompts import PROMPT_POS_TRADE_WIN
from ia.decision_parser import parse_decision, IADecision


def run_pos_trade_analysis(
    image_path: str,
    trade_data: dict,
    resumo_stats: str,
    llm_client
) -> IADecision:
    prompt = PROMPT_POS_TRADE_WIN.format(**trade_data, resumo_stats=resumo_stats)

    response = llm_client.run(prompt=prompt, image=image_path)

    if not response:
        raise RuntimeError("IA não retornou resposta")

    return parse_decision(response)
