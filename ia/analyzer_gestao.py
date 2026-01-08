# ia/analyzer_gestao.py

from ia.prompts import PROMPT_GESTAO_POSICAO_WIN
from ia.decision_parser import parse_decision, IADecision


def run_gestao_posicao(
    image_path: str,
    tipo_operacao: str,
    preco_entrada: float,
    preco_atual: float,
    pnl_atual: float,
    llm_client
) -> IADecision:
    prompt = PROMPT_GESTAO_POSICAO_WIN.format(
        tipo_operacao=tipo_operacao,
        preco_entrada=preco_entrada,
        preco_atual=preco_atual,
        pnl_atual=pnl_atual
    )

    response = llm_client.run(prompt=prompt, image=image_path)

    if not response:
        raise RuntimeError("IA não retornou resposta")

    return parse_decision(response)
