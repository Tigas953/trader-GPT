# main.py

print("🚀 Iniciando Trader GPT...")

import tkinter as tk

from core.state_manager import StateManager
from core.engine import Engine
from core.timer import ExecutionTimer
from ui.app import TraderGPTApp


def main():
    print("🚀 Iniciando Trader GPT...")

    state_manager = StateManager()
    timer = ExecutionTimer(cooldown_seconds=5)
    engine = Engine(state_manager, timer)

    print("Estado inicial:", engine.get_state_snapshot())

    engine.ligar_sistema()
    print("Após ligar sistema:", engine.get_state_snapshot())

    engine.abrir_trade()
    print("Após abrir trade:", engine.get_state_snapshot())

    engine.encerrar_trade()
    print("Após encerrar trade:", engine.get_state_snapshot())

    engine.concluir_pos_trade()
    print("Após concluir pós-trade:", engine.get_state_snapshot())


if __name__ == "__main__":
    main()
