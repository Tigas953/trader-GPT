# core/timer.py

import time


class ExecutionTimer:
    """
    Timer central de execução.
    Controla cooldown, concorrência e pausas automáticas.
    """

    def __init__(self, cooldown_seconds: int):
        self._cooldown = cooldown_seconds
        self._last_execution_ts: float | None = None
        self._running: bool = False
        self._paused: bool = False

    # =====================================================
    # CONTROLE DE EXECUÇÃO
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

        elapsed = time.time() - self._last_execution_ts
        return elapsed >= self._cooldown

    def start_execution(self):
        """
        Marca o início de uma execução.
        """
        if not self.can_execute():
            raise RuntimeError("Execução não permitida pelo Timer.")

        self._running = True

    def finish_execution(self):
        """
        Marca o fim de uma execução.
        """
        if not self._running:
            return

        self._running = False
        self._last_execution_ts = time.time()

    # =====================================================
    # PAUSA AUTOMÁTICA
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

    # =====================================================
    # MÉTODOS DE LEITURA (READ-ONLY)
    # =====================================================

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def is_paused(self) -> bool:
        return self._paused

    @property
    def cooldown_seconds(self) -> int:
        return self._cooldown

    @property
    def last_execution_time(self) -> float | None:
        return self._last_execution_ts

    def seconds_until_next_execution(self) -> int | None:
        """
        Retorna segundos restantes para próxima execução ou None se liberado.
        """
        if self._last_execution_ts is None:
            return None

        elapsed = time.time() - self._last_execution_ts
        remaining = self._cooldown - elapsed

        return max(0, int(remaining))
