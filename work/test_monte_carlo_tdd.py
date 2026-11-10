"""TDD vertical slice — monte_carlo Fase 3 (spec R1/R7/R8)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from work.monte_carlo import monte_carlo

def test_monte_carlo_structure():
    r = monte_carlo(seed=42, n_sims=100)
    assert r['phase'] == 3
    assert r['method'] == 'monte_carlo_with_costs'
    assert r['status'].startswith('INCONCLUSIVO'), "R1: nunca lucrativo sem prova"
    assert r['label'].startswith('SINTÉTICO'), "R5"
    assert len(r['hash_sha256']) == 16, "R8"
    assert r['costs']['spread'] > 0, "R7: custos realistas aplicados"
    assert r['seed'] == 42
