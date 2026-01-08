# core/engine.py

from core.state_manager import (
    StateManager,
    SystemMode,
    IAState,
    TradeState,
)


class Engine:
    """
    Engine é o cérebro do sistema.
    Nenhuma ação operacional acontece fora dela.
    """

    def __init__(self, state_manager: StateManager):
        self._state = state_manager

    # =====================================================
    # LEITURA DE ESTADO (PROXY SEGURO)
    # =====================================================

    def get_system_mode(self):
        return self._state.system_mode

    def get_ia_state(self):
        return self._state.ia_state

    def get_trade_state(self):
        return self._state.trade_state

    def is_system_on(self) -> bool:
        return self._state.system_on

    # =====================================================
    # VALIDAÇÕES DE EXECUÇÃO (PROMPTS)
    # =====================================================

    def can_run_pre_trade(self) -> bool:
        """
        Pré-trade só pode rodar se:
        - Sistema ligado
        - Nenhum trade ativo
        - IA não estiver bloqueada
        """
        return (
            self._state.system_on
            and self._state.trade_state == TradeState.INEXISTENTE
            and self._state.ia_state in [
                IAState.OCIOSA_MANUAL,
                IAState.OCIOSA_AUTOMATICA,
            ]
        )

    def can_run_gestao(self) -> bool:
        """
        Gestão de posição só pode rodar se:
        - Sistema ligado
        - Trade ABERTO
        - Solicitação manual (Engine apenas valida contexto)
        """
        return (
            self._state.system_on
            and self._state.trade_state == TradeState.ABERTO
            and self._state.ia_state != IAState.BLOQUEADA
        )

    def can_run_pos_trade(self) -> bool:
        """
        Pós-trade só pode rodar se:
        - Sistema ligado
        - Trade ENCERRADO
        """
        return (
            self._state.system_on
            and self._state.trade_state == TradeState.ENCERRADO
        )

    # =====================================================
    # EVENTOS DE SISTEMA
    # =====================================================

    def ligar_sistema(self):
        if self._state.system_on:
            return

        self._state.turn_system_on()

    def desligar_sistema(self):
        if not self._state.system_on:
            return

        self._state.turn_system_off()

    # =====================================================
    # EVENTOS DE TRADE
    # =====================================================

    def abrir_trade(self):
        """
        Chamado quando o usuário executa uma entrada manual.
        """
        if self._state.trade_state != TradeState.INEXISTENTE:
            raise RuntimeError("Trade já está ativo ou em estado inválido.")

        self._state.set_trade_state(TradeState.ABERTO)
        self._state.set_ia_state(IAState.GESTAO_POSICAO)

    def encerrar_trade(self):
        """
        Chamado quando o usuário encerra a posição.
        """
        if self._state.trade_state != TradeState.ABERTO:
            raise RuntimeError("Não existe trade aberto para encerrar.")

        self._state.set_trade_state(TradeState.ENCERRADO)
        self._state.set_ia_state(IAState.POS_TRADE)

    def concluir_pos_trade(self):
        """
        Chamado após a análise pós-trade ser finalizada.
        """
        if self._state.trade_state != TradeState.ENCERRADO:
            raise RuntimeError("Trade não está encerrado.")

        self._state.set_trade_state(TradeState.ANALISADO)
        self._state.reset_ia_to_idle()

    # =====================================================
    # EVENTOS DE IA (CONTROLE DE ESTADO)
    # =====================================================

    def iniciar_analise(self):
        """
        Usado antes de chamar QUALQUER IA.
        """
        if self._state.ia_state == IAState.ANALISANDO:
            raise RuntimeError("IA já está analisando.")

        self._state.set_ia_state(IAState.ANALISANDO)

    def finalizar_analise(self):
        """
        Usado após a IA terminar.
        """
        self._state.reset_ia_to_idle()
