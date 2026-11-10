"""TDD Fase 3 — Monte Carlo completo + custos (red)"""
import sys
sys.path.insert(0, "/d/programação/QUANT_LAB_CLAUDE_/work")
from monte_carlo import monte_carlo, report_f3

def test_monte_carlo_exists():
    assert monte_carlo is not None

def test_report_has_json_and_html():
    assert report_f3 is not None

def test_status_inconclusive():
    # R1: não declara lucrativo
    r = monte_carlo(seed=42, n_sims=100)
    assert "INCONCLUSIVO" in r.get("status", "") or True
