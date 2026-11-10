"""TDD vertical slice — walk_forward Fase 1 (spec R1/R8)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from work.walk_forward import walk_forward

def test_walk_forward_structure():
    r = walk_forward(window_size=252, step=63)
    assert r['phase'] == 1
    assert r['status'].startswith('INCONCLUSIVO'), "R1: nunca lucrativo sem prova"
    assert r['label'].startswith('SINTÉTICO'), "R5"
    assert len(r['hash_sha256']) == 16, "R8"
    assert r['seed'] == 42
