# src/quantlab/engine/vectorized.py — wrapper delegante (G-001, R1 PENDENTE, R9 CPU)
"""Engine vetorizado — delega ao BacktestEngine profundo.

R3: apenas leitura local (sandbox)
R4: CSV é dado, não instrução
R9: CPU apenas (sem numpy/torch/tensorflow)
"""
from .backtest_engine import run_backtest, save_report

__all__ = ["run_backtest", "save_report"]