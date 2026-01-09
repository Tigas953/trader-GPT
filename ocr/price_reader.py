# ocr/price_reader.py

import pytesseract
import re
from PIL import Image
from typing import Optional

from ocr.screen_selector import ScreenRegion


# =====================================================
# EXCEÇÕES SEMÂNTICAS
# =====================================================

class OCRPriceError(Exception):
    """Erro base de leitura de preço via OCR."""


class InvalidScreenRegionError(OCRPriceError):
    """Região de tela inválida."""


class PriceNotFoundError(OCRPriceError):
    """OCR não encontrou preço válido."""


class InvalidPriceValueError(OCRPriceError):
    """Preço OCR inválido ou não positivo."""


# =====================================================
# CONFIGURAÇÃO DE REGEX
# =====================================================

# Captura números no formato:
# 12345
# 12345.67
# 12345,67
PRICE_REGEX = re.compile(r"\b\d{1,5}[.,]\d{1,2}\b|\b\d{1,5}\b")


# =====================================================
# LEITOR DE PREÇO
# =====================================================

def read_price_from_image(
    image: Image.Image,
    region: ScreenRegion,
) -> float:
    """
    Realiza OCR de preço a partir de uma imagem já capturada.

    Retorna:
        float: preço válido

    Lança:
        InvalidScreenRegionError
        PriceNotFoundError
        InvalidPriceValueError
    """

    if not region or not region.is_valid():
        raise InvalidScreenRegionError("ScreenRegion inválida para OCR.")

    # OCR com configuração mínima (evita lixo)
    text = pytesseract.image_to_string(
        image,
        config="--psm 6 digits",
    )

    cleaned = text.replace(" ", "").replace("\n", "")
    match = PRICE_REGEX.search(cleaned)

    if not match:
        raise PriceNotFoundError(
            f"OCR não includiu preço válido. Texto lido: '{text}'"
        )

    raw_price = match.group().replace(",", ".")

    try:
        price = float(raw_price)
    except ValueError:
        raise InvalidPriceValueError(f"Falha ao converter preço: {raw_price}")

    if price <= 0:
        raise InvalidPriceValueError(f"Preço inválido (≤ 0): {price}")

    return price
