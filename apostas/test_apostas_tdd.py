"""TDD — Apostas Esportivas (Domínio C)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_apostas_sandbox():
    assert not os.path.exists('.env'), "R3"
    assert True
