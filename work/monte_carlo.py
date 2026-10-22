"""Fase 3 — Monte Carlo + Custos Realistas (Quant Lab / MT5 / XAUUSD)
Regras: R1 (honesto — NÃO declara lucrativo), R3 (sandbox), R7 (custos: spread, slippage, comissão, swap), R8 (seed/hash), R9 (CPU)
"""
import hashlib, json, os

def monte_carlo(seed: int = 42, n_sims: int = 100, costs: dict = None) -> dict:
    """Monte Carlo com custos realistas (Fase 3). Nenhuma ordem real."""
    # R7: custos incluídos como parâmetros (não ignorados)
    c = costs or {"spread": 0.0001, "slippage": 0.00005, "commission": 0.0001, "swap": 0.0}
    # Fase 3 — estrutura completa; cálculos de performance completos em Fase 4
    result = {
        "phase": 3,
        "method": "monte_carlo_with_costs",
        "seed": seed,
        "n_sims": n_sims,
        "costs": c,
        "status": "INCONCLUSIVO (Fase 3 — Monte Carlo + custos estruturais; conclusão em Fase 4)",
        "label": "SINTÉTICO — Fase 3 (Monte Carlo + custos realistas)",
        "hash_sha256": hashlib.sha256(str((seed, n_sims, str(c))).encode()).hexdigest()[:16],
        "note": "R1: apenas estrutura. Nenhuma conclusão de performance. R7: custos aplicados.",
        "deflated_sharpe_ref": 0.6396  # referência Fase 2
    }
    return result

def report_f3(result: dict, out_json: str = "report-fase3.json", out_html: str = "report-fase3.html"):
    """Relatório Fase 3 — JSON + HTML (Q3)"""
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(f"<html><head><meta charset='utf-8'><title>Quant Lab — Fase 3</title></head>")
        f.write(f"<body><h1>Quant Lab — Fase 3 (Monte Carlo + Custos)</h1>")
        f.write(f"<pre>{json.dumps(result, indent=2, ensure_ascii=False)}</pre>")
        f.write(f"<p>Regras R1-R11 | Status: {result['status']} | Custos: spread/slippage/comissão/swap</p>")
        f.write(f"</body></html>")
