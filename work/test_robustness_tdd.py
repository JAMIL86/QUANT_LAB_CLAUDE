"""TDD vertical slice — robustez Fase 2 (Monte Carlo + Deflated Sharpe)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from work.deflated_sharpe import deflated_sharpe, pbo_estimate
from work.monte_carlo import monte_carlo

def test_robustness_combined():
    mc = monte_carlo(42, 100)
    ds = deflated_sharpe(0.6396, trials=mc['n_sims'])
    pbo = pbo_estimate(trials=mc['n_sims'])
    assert mc['status'].startswith('INCONCLUSIVO')  # R1
    assert ds['status'].startswith('INCONCLUSIVO')  # R1
    assert len(mc['hash_sha256']) == 16 and len(ds['hash_sha256']) == 16  # R8
    assert mc['costs']['spread'] > 0  # R7
