"""Validation module — Quant Lab
Regras: R1 honesto, R3 sandbox, R6 sem look-ahead, R8 seed/hash, R9 CPU
"""
from .walk_forward import walk_forward_validate

__all__ = ["walk_forward_validate"]