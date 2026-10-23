"""Monte Carlo module — Quant Lab
Regras: R1 honesto, R3 sandbox, R7 custos realistas, R8 seed/hash, R9 CPU
"""
from .engine import monte_carlo, report_f3

__all__ = ["monte_carlo", "report_f3"]