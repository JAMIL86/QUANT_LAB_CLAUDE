# src/quantlab/ingest/ocr_stub.py — stub avançado (não instala Tesseract)
"""Stub OCR (ticket 6) — sem Tesseract/pdfminer pesado (R9 respeitado)."""

def detect_pdf_magic(path: str) -> bool:
    with open(path, 'rb') as f:
        header = f.read(5)
    return header.startswith(b'%PDF')

def extract_text_from_pdf(path: str) -> str:
    """Stub — em produção: Tesseract/pdfminer (com aprovacão)."""
    if not detect_pdf_magic(path):
        raise ValueError("Arquivo nao e PDF (detectado por magic bytes).")
    return "STUB: texto extraido de PDF (simulacao para testes de laboratorio, R5 sintético)."

def extract_text_from_image(path: str) -> str:
    return "STUB: OCR de imagem (simulacao — nao usa Tesseract). R5: sintético."
