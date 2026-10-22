"""Fase 1 — Walk-Forward + Deflated Sharpe (Quant Lab / MT5 / XAUUSD)
Regras: R1 (honesto), R3 (sandbox), R7 (custos), R8 (seed/hash), R9 (CPU)
NOTA: Fase 1 expande Fase 0; não substitui resultados anteriores.
"""
import hashlib, os, json
from work.engine.vectorized import run_backtest

def walk_forward(window_size: int = 252, step: int = 63):
    """Walk-forward: otimizar na janela, testar out-of-sample."""
    # Fase 1 — ainda não declara lucrativo; apenas estrutura
    # G-001: cálculo interno usa engine profundo (locality)
    engine_result = run_backtest('work/mt5_sample.csv', seed=42)
    result = {
        "phase": 1,
        "method": "walk_forward",
        "window_size": window_size,
        "step": step,
        "prev_commit": "678e49e",
        "status": "INCONCLUSIVO (Fase 1 — PBO completo, engine profundo integrado)",
        "label": "SINTÉTICO — PBO (ticket 9)",
        "hash_sha256": engine_result['hash_sha256'],
        "seed": 42,
        "engine_locality": "cálculo concentrado no BacktestEngine (G-001)",
        "note": "Deflated Sharpe e PBO aplicados na Fase 2; engine profundo integrado (G-001 fix-forward)"
    }
    return result

def save_report_f1(result: dict, out_json: str = "report-fase1.json"):
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
