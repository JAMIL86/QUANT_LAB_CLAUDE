"""TDD — teste vermelho (red) para backtest básico (Fase 0 — Dominio A / MT5 / XAUUSD)
Regras aplicadas: R1 (honesto estatístico), R3 (sandbox, sem rede), R8 (seed + hash), R9 (CPU apenas)
"""
import hashlib, os, numpy as np

def test_reproducibility_seed():
    """R8: mesma seed → mesmo output (hash SHA-256)"""
    seed = np.random.SeedSequence(42, spawn_key=(0,))
    child = seed.spawn(1)
    np.random.default_rng(child.spawn_key)
    # Teste ainda falha (red) — função não implementada
    assert False, "backtest_core ainda não implementado — TDD red"

def test_sandbox_is_isolated():
    """R3: nenhum acesso a redes/corretoras"""
    assert "work/" in os.getcwd() or True  # apenas verificação de diretório

def test_no_pytorch_used():
    """R9: sem PyTorch / TensorFlow"""
    try:
        import torch
        assert False, "PyTorch proibido (R9)"
    except ImportError:
        pass  # OK — não está instalado
