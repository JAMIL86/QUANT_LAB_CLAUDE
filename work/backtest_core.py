"""Backtest básico — Fase 0 (Quant Lab / Domínio A / MT5 / XAUUSD)
Regras: R1 honesto, R3 sandbox, R8 seed/hash, R9 CPU apenas, R11 PT-BR docs
"""
import hashlib, os, json

def run_backtest(path_csv: str, seed: int = 42) -> dict:
    """Executa backtest básico em arquivo CSV local (sandbox). Nenhuma ordem real."""
    # R8: seed controlada
    rng = None  # R9: CPU, sem numpy quando não disponível
    # R3: apenas leitura — nenhum acesso a corretora
    # R9: CPU somente, chunks pequenas (não PyTorch)
    # R7: custos ainda não aplicados (Fase 0 básico)
    # R1: resultado ainda não declara "lucrativo" — apenas métrica básica
    
    # Simulação simples: retorna métricas básicas (não conclusão)
    result = {
        "source_file": path_csv,
        "seed": seed,
        "hash_sha256": hashlib.sha256(str(seed).encode()).hexdigest()[:16],
        "status": "INCONCLUSIVO (Fase 0 — dados básicos apenas)",
        "metrics": {"sharpe": None, "drawdown_max": None, "trades": 0},
        "label": "SINTÉTICO — para testes do laboratório apenas"
    }
    return result

def save_report(result: dict, out_json: str, out_html: str = None):
    """R8 + Q3: JSON fonte de verdade + HTML leitura"""
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    # HTML básico (não marketing — lab técnico, dials 3/2/5)
    if out_html:
        with open(out_html, "w", encoding="utf-8") as f:
            f.write(f"<html><head><meta charset='utf-8'><title>Quant Lab — Fase 0</title></head>")
            f.write(f"<body><h1>Quant Lab — Backtest Fase 0</h1><pre>{json.dumps(result, indent=2)}</pre>")
            f.write(f"<p>Regras: R1-R11 | Status: {result['status']} | Label: {result['label']}</p></body></html>")
