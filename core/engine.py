# core/engine.py

from core.state_manager import StateManager, InvalidStateTransition


class Engine:
    """
    Engine é o cérebro do sistema.
    Nenhuma ação operacional acontece fora dela.
    Ela NÃO executa IA, apenas autoriza ou bloqueia.
    """

    def __init__(self, state_manager: StateManager, timer):
        self._state = state_manager
        self._timer = timer

    # =====================================================
    # LEITURA DE ESTADO (SOMENTE LEITURA)
    # =====================================================

    def get_state_snapshot(self) -> dict:
        """
        Fotografia imutável do estado atual do sistema.
        Usado por UI, logs e debug.
        """
        return {
            "system_on": self._state.is_system_on(),
            "system_mode": self._state.get_system_mode().name,
            "ia_state": self._state.get_ia_state().name,
            "trade_state": self._state.get_trade_state().name,
            "cooldown_ok": self._timer.can_execute(),
        }

    # =====================================================
    # EVENTOS DE SISTEMA
    # =====================================================

    def ligar_sistema(self):
        if self._state.is_system_on():
            return
        self._state.power_on()

    def desligar_sistema(self):
        if not self._state.is_system_on():
            return
        self._state.power_off()

    # =====================================================
    # EVENTOS DE TRADE
    # =====================================================

    def abrir_trade(self):
        self._state.open_trade()

    def encerrar_trade(self):
        self._state.close_trade()

    def concluir_pos_trade(self):
        self._state.mark_trade_analyzed()
        self._state.reset_trade()

    # =====================================================
    # AUTORIZAÇÃO DE IA (SEM EXECUTAR IA)
    # =====================================================

    def authorize_pre_trade(self):
        if not self._timer.can_execute():
            raise RuntimeError("Cooldown ativo.")
        self._state.start_pre_trade()
        self._timer.mark_execution_start()

    def authorize_gestao_posicao(self):
        if not self._timer.can_execute():
            raise RuntimeError("Cooldown ativo.")
        self._state.start_gestao_posicao()
        self._timer.mark_execution_start()

    def authorize_pos_trade(self):
        if not self._timer.can_execute():
            raise RuntimeError("Cooldown ativo.")
        self._state.start_pos_trade()
        self._timer.mark_execution_start()

    def finalizar_analise(self):
        """
        Deve ser chamado SEMPRE após a IA terminar.
        """
        self._state.finish_analysis()
        self._timer.mark_execution_end()
