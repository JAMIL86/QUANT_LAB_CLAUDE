"""Fase 2 — Deflated Sharpe + PBO (Quant Lab / MT5 / XAUUSD)
Regras: R1 (honesto — NÃO declara lucrativo sem CI), R3 (sandbox), R8 (seed/hash), R9 (CPU)
"""
import hashlib, math, json, os


def deflated_sharpe(sharpe_raw: float, trials: int, n_years: int = 5) -> dict:
    """Deflated Sharpe corrigido por múltiplas hipóteses (López de Prado)."""
    # Simplificação Fase 2 — estrutura correta; cálculo completo em Fase 3
    n = max(trials, 1)
    deflated = sharpe_raw * math.sqrt(1 - (n - 1) / (n + 1)) if n > 1 else sharpe_raw
    return {
        "phase": 2,
        "method": "deflated_sharpe_pbo",
        "sharpe_raw": sharpe_raw,
        "deflated_sharpe": round(deflated, 4),
        "trials": trials,
        "n_years": n_years,
        "status": "INCONCLUSIVO (Fase 2 — Deflated Sharpe estrutural; cálculo completo em Fase 3)",
        "label": "SINTÉTICO — Fase 2 (Monte Carlo + Deflated Sharpe + PBO)",
        "hash_sha256": hashlib.sha256(str((sharpe_raw, trials)).encode()).hexdigest()[:16],
        "seed": 42,
        "note": "R1: apenas estrutura. Nenhuma conclusão de performance."
    }

def pbo_estimate(trials: int, n_years: int = 5) -> dict:
    """Probability of Backtest Overfitting (PBO) — estimativa."""
    return {
        "phase": 2,
        "method": "pbo",
        "trials": trials,
        "pbo_estimate": min(0.5 + 0.05 * max(0, trials - 5), 0.95),  # simplificada
        "status": "INCONCLUSIVO (estimativa Fase 2)",
        "label": "SINTÉTICO — PBO (Fase 2)"
    }

__all__ = ["deflated_sharpe", "pbo_estimate"]