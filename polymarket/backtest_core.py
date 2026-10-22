"""Backtest Polymarket — Domínio B (sandbox, R3, R1, R5, R8)"""
import hashlib, csv, random

def run_backtest(path_csv="/d/programação/QUANT_LAB_CLAUDE_/work/mt5_sample.csv", seed=42):
    random.seed(seed)
    with open(path_csv, newline='') as f:
        rows = list(csv.DictReader(f))
    trades = len(rows)
    result = {
        "phase": "B",
        "domain": "polymarket",
        "seed": seed,
        "hash_sha256": hashlib.sha256(str(seed).encode()).hexdigest()[:16],
        "status": "INCONCLUSIVO (Domínio B — dados básicos)",
        "metrics": {"trades": trades},
        "label": "SINTÉTICO — Polymarket (R5)",
        "rules": ["R1","R3","R5","R8","R9"]
    }
    return result
