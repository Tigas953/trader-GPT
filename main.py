# main.py

from core.state_manager import StateManager
from core.engine import Engine
from core.timer import ExecutionTimer
from ui.app import TraderGPTApp


def main():
    print("🚀 Iniciando Trader GPT...")

    # 1️⃣ Estado central (fonte da verdade)
    state_manager = StateManager()

    # 2️⃣ Timer central (controle de concorrência)
    timer = ExecutionTimer(cooldown_seconds=5)

    # 3️⃣ Engine (cérebro do sistema)
    engine = Engine(state_manager, timer)

    # 4️⃣ UI (espelho do sistema)
    app = TraderGPTApp(engine)

    # 5️⃣ Iniciar aplicação
    app.run()


if __name__ == "__main__":
    main()
