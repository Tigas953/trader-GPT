# ocr/price_reader.py

import pytesseract
import re
from PIL import ImageGrab
from typing import Optional
from ocr.screen_selector import ScreenRegion


PRICE_REGEX = re.compile(r"\d+[.,]?\d*")


def read_price(region: ScreenRegion) -> float:
    """
    Realiza OCR do preço na região informada.
    Retorna float válido ou lança exceção.
    """
    image = ImageGrab.grab(
        bbox=(
            region.x,
            region.y,
            region.x + region.width,
            region.y + region.height,
        )
    )

    text = pytesseract.image_to_string(image)
    match = PRICE_REGEX.search(text.replace(" ", ""))

    if not match:
        raise ValueError("OCR não identificou preço válido")

    raw_price = match.group().replace(",", ".")

    try:
        price = float(raw_price)
    except ValueError:
        raise ValueError("Preço OCR inválido")

    if price <= 0:
        raise ValueError("Preço OCR não positivo")

    return price
