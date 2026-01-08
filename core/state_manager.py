# core/state_manager.py
from enum import Enum, auto


# =====================================================
# ENUMS — CONTRATO FORMAL DE ESTADO
# =====================================================

class SystemMode(Enum):
    OBSERVACAO = auto()
    MANUAL = auto()
    AUTOMATICO = auto()


class IAState(Enum):
    DESLIGADA = auto()
    OCIOSA = auto()
    ANALISANDO_PRE_TRADE = auto()
    GESTAO_POSICAO = auto()
    POS_TRADE = auto()
    BLOQUEADA = auto()


class TradeState(Enum):
    INEXISTENTE = auto()
    ABERTO = auto()
    ENCERRADO = auto()
    ANALISADO = auto()


# =====================================================
# EXCEÇÃO ESPECÍFICA DE ESTADO
# =====================================================

class InvalidStateTransition(Exception):
    """Erro lançado quando uma transição de estado ilegal é solicitada."""
    pass


# =====================================================
# STATE MANAGER — ÚNICA AUTORIDADE DE ESTADO
# =====================================================

class StateManager:
    def __init__(self):
        # Estado inicial obrigatório
        self._system_mode = SystemMode.MANUAL
        self._ia_state = IAState.DESLIGADA
        self._trade_state = TradeState.INEXISTENTE

    # =================================================
    # READ-ONLY GETTERS
    # =================================================

    def get_system_mode(self):
        return self._system_mode

    def get_ia_state(self):
        return self._ia_state

    def get_trade_state(self):
        return self._trade_state

    # =================================================
    # FLAGS DE CONVENIÊNCIA (READ-ONLY)
    # =================================================

    def is_system_on(self):
        return self._ia_state != IAState.DESLIGADA

    def is_trade_open(self):
        return self._trade_state == TradeState.ABERTO

    def is_ia_busy(self):
        return self._ia_state in {
            IAState.ANALISANDO_PRE_TRADE,
            IAState.GESTAO_POSICAO,
            IAState.POS_TRADE,
        }

    # =================================================
    # VERIFICAÇÃO DE PERMISSÃO DE PROMPTS
    # =================================================

    def can_run_pre_trade(self):
        return (
            self._trade_state == TradeState.INEXISTENTE and
            self._ia_state == IAState.OCIOSA
        )

    def can_run_gestao_posicao(self):
        return (
            self._trade_state == TradeState.ABERTO and
            self._ia_state == IAState.OCIOSA
        )

    def can_run_pos_trade(self):
        return (
            self._trade_state == TradeState.ENCERRADO and
            self._ia_state == IAState.OCIOSA
        )

    # =================================================
    # TRANSIÇÕES DE ESTADO — SISTEMA
    # =================================================

    def set_system_mode(self, new_mode: SystemMode):
        if self.is_system_on():
            raise InvalidStateTransition(
                "Modo do sistema só pode ser alterado com o sistema desligado."
            )
        self._system_mode = new_mode

    # =================================================
    # TRANSIÇÕES DE ESTADO — IA
    # =================================================

    def power_on(self):
        if self._ia_state != IAState.DESLIGADA:
            raise InvalidStateTransition("Sistema já está ligado.")
        self._ia_state = IAState.OCIOSA

    def power_off(self):
        self._ia_state = IAState.DESLIGADA

    def start_pre_trade(self):
        if not self.can_run_pre_trade():
            raise InvalidStateTransition("Pré-trade não permitido neste estado.")
        self._ia_state = IAState.ANALISANDO_PRE_TRADE

    def start_gestao_posicao(self):
        if not self.can_run_gestao_posicao():
            raise InvalidStateTransition("Gestão de posição não permitida.")
        self._ia_state = IAState.GESTAO_POSICAO

    def start_pos_trade(self):
        if not self.can_run_pos_trade():
            raise InvalidStateTransition("Pós-trade não permitido.")
        self._ia_state = IAState.POS_TRADE

    def finish_analysis(self):
        if self._ia_state not in {
            IAState.ANALISANDO_PRE_TRADE,
            IAState.GESTAO_POSICAO,
            IAState.POS_TRADE,
        }:
            raise InvalidStateTransition("Nenhuma análise em execução.")
        self._ia_state = IAState.OCIOSA

    def block_ia(self):
        self._ia_state = IAState.BLOQUEADA

    def unblock_ia(self):
        if self._ia_state != IAState.BLOQUEADA:
            raise InvalidStateTransition("IA não está bloqueada.")
        self._ia_state = IAState.OCIOSA

    # =================================================
    # TRANSIÇÕES DE ESTADO — TRADE
    # =================================================

    def open_trade(self):
        if self._trade_state != TradeState.INEXISTENTE:
            raise InvalidStateTransition("Já existe um trade ativo.")
        self._trade_state = TradeState.ABERTO

    def close_trade(self):
        if self._trade_state != TradeState.ABERTO:
            raise InvalidStateTransition("Nenhum trade aberto para encerrar.")
        self._trade_state = TradeState.ENCERRADO

    def mark_trade_analyzed(self):
        if self._trade_state != TradeState.ENCERRADO:
            raise InvalidStateTransition("Trade não está pronto para análise.")
        self._trade_state = TradeState.ANALISADO

    def reset_trade(self):
        if self._trade_state != TradeState.ANALISADO:
            raise InvalidStateTransition("Trade não pode ser resetado ainda.")
        self._trade_state = TradeState.INEXISTENTE
