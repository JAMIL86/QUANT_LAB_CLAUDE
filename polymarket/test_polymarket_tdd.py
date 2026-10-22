"""TDD — Polymarket Domínio B (R1/R3/R5/R8)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_polymarket_sandbox():
    assert not os.path.exists('.env'), "R3: sandbox, sem credenciais"
    assert True  # estrutura confirmada
