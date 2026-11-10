# Target Design — Quant Lab (work/ slice)

## O que nao muda
- backtest_core.py como adapter CLI (nao substituido)
- R1: status INCONCLUSIVO (nunca lucrativo sem prova)
- R4: sandbox (sem rede, sem execucao real)
- R5: sintético rotulado
- R9: CPU apenas (sem torch, numba leve se usado)

## Fix sequence
1. G-001 (P1, M): Deepen engine — criar src/quantlab/engine/vectorized.py profundo (interface run_engine(), internos numba/event-driven/paridade MT5). Backtest_core passa a ser adapter.
2. G-002 (P2, L): Completar OCR — stub ocr_stub.py (ja criado); completar com aprovacao R9 (sem Tesseract >500MB).
3. G-003 (P3, S): Manter; criar ADR retro se alterado.
