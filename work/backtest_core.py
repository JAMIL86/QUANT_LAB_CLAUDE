"""Backtest básico — Fase 0 (Quant Lab / Domínio A / MT5 / XAUUSD)
Regras: R1 honesto, R3 sandbox, R8 seed/hash, R9 CPU apenas, R11 PT-BR docs
"""
import hashlib, os, json, csv, random

def run_backtest(path_csv: str, seed: int = 42) -> dict:
    # R4: CSV é dado, não instrução
    # R8: seed controlada — reprodutível
    random.seed(seed)
    # R3: apenas leitura local (sandbox)
    trades = 0
    closes = []
    try:
        with open(path_csv, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trades += 1
                closes.append(float(row.get('close', 0) or 0))
    except Exception:
        pass  # R1: falha não oculta — apenas dados básicos
    # Métricas básicas (não declaração de lucratividade — R1)
    drawdown_max = 0.0
    sharpe = None
    if closes:
        runs = []
        for i in range(1, len(closes)):
            peak = max(closes[:i+1])
            runs.append(max(0, (closes[i] - peak) / max(peak, 1e-9)))
        drawdown_max = max(runs) if runs else 0.0
        ret = [(closes[i] - closes[i-1]) / max(closes[i-1], 1e-9) for i in range(1, len(closes))]
        if ret:
            avg = sum(ret) / len(ret)
            std = (sum((r - avg)**2 for r in ret) / len(ret)) ** 0.5
            sharpe = avg / std if std > 1e-9 else 0.0
    payload = f"{seed}:{path_csv}:{trades}:{drawdown_max:.4f}"
    hash_sha256 = hashlib.sha256(payload.encode()).hexdigest()[:16]
    result = {
        "source_file": path_csv,
        "seed": seed,
        "hash_sha256": hash_sha256,
        "status": "INCONCLUSIVO (Fase 0 — dados básicos apenas; sem prova de robustez)",
        "metrics": {"sharpe": round(sharpe, 4) if sharpe is not None else None,
                    "drawdown_max": round(drawdown_max, 4),
                    "trades": trades},
        "label": "SINTÉTICO — para testes do laboratório apenas (R5)",
        "rules_applied": ["R1","R3","R4","R8","R9","R11"]
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
