# core/timer.py

import time
from threading import Lock


class ExecutionTimer:
    """
    Timer central de execução.

    Responsabilidades:
    - Impedir execuções concorrentes
    - Controlar cooldown entre análises
    - Permitir pausa operacional (ex: trade aberto, observação)
    - Expor estado somente leitura
    """

    def __init__(self, cooldown_seconds: int):
        self._cooldown = cooldown_seconds
        self._last_execution_ts: float | None = None
        self._running: bool = False
        self._paused: bool = False
        self._lock = Lock()

    # =====================================================
    # CONSULTAS (READ-ONLY)
    # =====================================================

    def can_execute(self) -> bool:
        """
        Retorna True se uma nova execução pode iniciar.
        """
        if self._paused:
            return False

        if self._running:
            return False

        if self._last_execution_ts is None:
            return True

        return (time.time() - self._last_execution_ts) >= self._cooldown

    def is_running(self) -> bool:
        return self._running

    def is_paused(self) -> bool:
        return self._paused

    def remaining_cooldown(self) -> float:
        """
        Retorna segundos restantes de cooldown (0 se liberado).
        """
        if self._last_execution_ts is None:
            return 0.0

        elapsed = time.time() - self._last_execution_ts
        return max(0.0, self._cooldown - elapsed)

    # =====================================================
    # CONTROLE DE EXECUÇÃO (ATÔMICO)
    # =====================================================

    def start_execution(self):
        """
        Marca início de execução.
        Deve ser chamado IMEDIATAMENTE antes da IA.
        """
        with self._lock:
            if not self.can_execute():
                raise RuntimeError("Execução não permitida pelo Timer.")

            self._running = True

    def finish_execution(self):
        """
        Marca fim de execução.
        Deve ser chamado SEMPRE em bloco finally.
        """
        with self._lock:
            if not self._running:
                return

            self._running = False
            self._last_execution_ts = time.time()

    # =====================================================
    # PAUSA OPERACIONAL
    # =====================================================

    def pause(self):
        """
        Pausa o timer (ex: trade aberto, modo observação).
        """
        self._paused = True

    def resume(self):
        """
        Retoma o timer.
        """
        self._paused = False
