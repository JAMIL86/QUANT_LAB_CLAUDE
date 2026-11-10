"""TDD — G-001 fix-forward: engine profundo (red antes, green depois)
R1: nunca lucrativo; R8: seed/hash reprodutível; R9: CPU/numpy; R5: SINTÉTICO"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from work.engine.vectorized import run_backtest


def test_engine_deep_locality_and_leverage():
    """G-001: módulo profundo concentra cálculo; interface única preservada"""
    result = run_backtest('work/mt5_sample.csv', seed=42)
    assert result['label'] == 'SINTETICO', "R5 quebrado"
    assert result['status'].startswith('INCONCLUSIVO'), "R1 quebrado: nunca lucrativo"
    assert len(result['hash_sha256']) == 16, "R8 quebrado: hash deve ter 16 chars"
    assert result['seed'] == 42, "R8 quebrado: seed não preservado"
    assert result['sharpe'] == 0.01
    assert result['drawdown_max'] == 0.005
    # Leverage: uma interface, múltiplas métricas retornadas (locality confirmada)
    assert 'trades' in result
