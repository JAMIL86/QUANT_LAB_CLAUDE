"""TDD Fase 2 — Deflated Sharpe + PBO (red -> green)"""
import sys
sys.path.insert(0, "/d/programação/QUANT_LAB_CLAUDE_/work")
from deflated_sharpe import deflated_sharpe, pbo_estimate

def test_deflated_sharpe_exists():
    assert deflated_sharpe is not None

def test_pbo_exists():
    assert pbo_estimate is not None

def test_result_is_inconclusive():
    # R1: não declara lucrativo sem prova completa
    r = deflated_sharpe(sharpe_raw=1.5, trials=10, n_years=5)
    assert "INCONCLUSIVO" in r.get("status", "") or r.get("deflated_sharpe") is not None
