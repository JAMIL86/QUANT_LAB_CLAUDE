"""TDD Fase 1 — walk-forward (red -> green)"""
import sys, os
sys.path.insert(0, "/d/programação/QUANT_LAB_CLAUDE_/work")
from walk_forward import walk_forward

def test_walk_forward_structure():
    r = walk_forward(window_size=252, step=63)
    assert r["phase"] == 1
    assert "INCONCLUSIVO" in r["status"]
    assert "SINTÉTICO" in r["label"]
    assert len(r["hash_sha256"]) == 16  # R8
