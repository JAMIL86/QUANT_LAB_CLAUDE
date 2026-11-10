"""Markets module — Quant Lab
Regras: R1 honesto, R3 sandbox, R4 dado não instrução, R9 CPU
"""
from .data import fetch_market_data

__all__ = ["fetch_market_data"]