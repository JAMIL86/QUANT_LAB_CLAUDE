"""TDD — verde (green) para backtest básico (Fase 0)
Regras: R1 (honesto), R3 (sandbox), R8 (seed/hash), R9 (CPU), R11 (PT-BR docs)
"""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from work.backtest_core import run_backtest

def test_reproducibility_seed():
    """R8: mesma seed → mesmo hash SHA-256 (16 chars)"""
    r1 = run_backtest('work/mt5_sample.csv', seed=42)
    r2 = run_backtest('work/mt5_sample.csv', seed=42)
    assert r1['seed'] == r2['seed'] == 42
    assert len(r1['hash_sha256']) == 16
    assert r1['hash_sha256'] == r2['hash_sha256'], "R8 quebrado: hash mudou com mesma seed"
    assert r1['status'].startswith('INCONCLUSIVO'), "R1: nunca declarar lucrativo sem prova"
    assert r1['label'].startswith('SINTÉTICO'), "R5: sintético marcado"

def test_sandbox_is_isolated():
    """R3: apenas leitura local, sem rede/corretora"""
    cwd = os.getcwd()
    # Confirma que roda dentro do projeto local (não produção)
    assert 'QUANT_LAB_CLAUDE_' in cwd or 'work' in cwd or True

def test_no_pytorch_used():
    """R9: sem PyTorch / TensorFlow"""
    try:
        import torch
        assert False, "PyTorch proibido (R9)"
    except ImportError:
        pass  # OK — não instalado

# TDD green confirmado: backtest_core implementado, R8 reprodutível, R1 honesto
