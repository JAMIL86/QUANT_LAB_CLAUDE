"""Metrics module — Quant Lab
Regras: R1 honesto, R3 sandbox, R8 seed/hash, R9 CPU
"""
from .deflated_sharpe import deflated_sharpe, pbo_estimate

__all__ = ["deflated_sharpe", "pbo_estimate"]