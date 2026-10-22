"""Fase 1 — Walk-Forward + Deflated Sharpe (Quant Lab / MT5 / XAUUSD)
Regras: R1 (honesto), R3 (sandbox), R7 (custos), R8 (seed/hash), R9 (CPU)
NOTA: Fase 1 expande Fase 0; não substitui resultados anteriores.
"""
import hashlib, os, json
from backtest_core import run_backtest, save_report

def walk_forward(window_size: int = 252, step: int = 63):
    """Walk-forward: otimizar na janela, testar out-of-sample."""
    # Fase 1 — ainda não declara lucrativo; apenas estrutura
    result = {
        "phase": 1,
        "method": "walk_forward",
        "window_size": window_size,
        "step": step,
        "status": "INCONCLUSIVO (Fase 1 — estrutura apenas)",
        "label": "SINTÉTICO — Fase 1 (walk-forward) — testes de laboratório",
        "hash_sha256": hashlib.sha256(str(window_size).encode()).hexdigest()[:16],
        "seed": 42,
        "note": "Deflated Sharpe e PBO aplicados na Fase 2"
    }
    return result

def save_report_f1(result: dict, out_json: str = "report-fase1.json"):
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
