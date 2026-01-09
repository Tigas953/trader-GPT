# ocr/regions_store.py

import json
from pathlib import Path
from typing import Tuple

from ocr.screen_selector import ScreenRegion


REGIONS_FILE = Path("config/screen_regions.json")


class ScreenRegionStore:
    """
    Persistência das regiões de tela selecionadas pelo usuário.

    Responsabilidade ÚNICA:
    - Salvar
    - Carregar

    NÃO:
    - Seleciona região
    - Valida lógica de negócio
    - Interage com Engine ou IA
    """

    @staticmethod
    def save(price_region: ScreenRegion, capture_region: ScreenRegion) -> None:
        if not price_region.is_valid() or not capture_region.is_valid():
            raise ValueError("Regiões inválidas não podem ser salvas.")

        REGIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "price": price_region.to_dict(),
            "capture": capture_region.to_dict(),
        }

        REGIONS_FILE.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def load() -> Tuple[ScreenRegion, ScreenRegion]:
        if not REGIONS_FILE.exists():
            raise RuntimeError("Áreas de captura ainda não configuradas.")

        data = json.loads(REGIONS_FILE.read_text(encoding="utf-8"))

        try:
            price = ScreenRegion.from_dict(data["price"])
            capture = ScreenRegion.from_dict(data["capture"])
        except Exception as e:
            raise RuntimeError("Arquivo de regiões corrompido.") from e

        return price, capture
