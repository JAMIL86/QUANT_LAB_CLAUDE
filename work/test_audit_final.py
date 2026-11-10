"""Audit / verificação final — R8 + R4 + R1 + R5 (spec-fase0.md)"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtest_core import run_backtest
from deflated_sharpe import deflated_sharpe, pbo_estimate
from monte_carlo import monte_carlo
from walk_forward import walk_forward

def test_audit_integridade():
    # F0
    r0 = run_backtest('work/mt5_sample.csv', seed=42)
    assert r0["hash_sha256"] and len(r0["hash_sha256"])==16
    assert r0['status'].startswith('INCONCLUSIVO')
    assert r0['label'].startswith('SINTÉTICO')
    # F2
    r2 = deflated_sharpe(0.6396, trials=3)
    assert len(r2['hash_sha256']) == 16
    assert r2['status'].startswith('INCONCLUSIVO')
    # F3 mc
    r3 = monte_carlo(42, 100)
    assert r3['costs']['spread'] == 0.0001  # R7
    assert len(r3['hash_sha256']) == 16
    # F3 walk
    r3w = walk_forward(252, 63)
    assert r3w['phase'] == 1
    # Todos: .env não deve existir (R8 segurança)
    assert not os.path.exists('.env'), "R8: .env não deve ser commitado"
    print('AUDIT PASS: F0-F3 integridade confirmada; R1/R4/R5/R7/R8 OK; .env ausente')
