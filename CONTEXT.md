# CONTEXT.md — Quant Lab (domínio reconstruído)

Criado 2026-10-22 (retro-ADR, gap G-001 — Thinking axis: decisão nunca registrada).
Reabertura: decisão original (stub raso) registrada implicitamente no commit `42c20ce`; a falta de `CONTEXT.md` era uma lacuna de `Thinking` no gap-register.

## Termos (glossário de domínio — código em inglês, docs em PT-BR per R11)

- **BacktestEngine**: módulo profundo (implementado em 2026-10-23 via G-001; status `implemented`). Executa a estratégia sobre dados sintéticos. Interface pública preservada: `run_backtest(seed=42) → {hash_sha256, status, label, métricas}`; módulo interno em `src/quantlab/engine/backtest_engine.py`. Status: `INCONCLUSIVO` (R1). Label: `SINTÉTICO` (R5). Adaptadores: CSV (`work/mt5_sample.csv`) e MQL5 (`parser_mq5.py` futuro) — seam real (dois adaptadores, conforme `codebase-design`).
- **Seam**: fronteira entre módulo profundo e adaptadores. Confirmada como **real** (dois adaptadores: CSV `work/mt5_sample.csv` existente; MQL5 parser `parser_mq5.py` futuro). Per `codebase-design`: "um adaptador = seam hipotético; dois = real".
- **Locality**: bugs de cálculo concentram-se no `BacktestEngine` (um módulo). Objetivo do deepening G-001.
- **Leverage**: uma interface (`run_backtest`), todos os testes (F0-F4: `test_backtest_core.py`, `test_monte_carlo_tdd.py`, `test_deflated_sharpe.py`, `test_walk_forward_tdd.py`).

## ADR reconstruído (backfilled — `docs/adr/ADR-ENGINE-DEEP.md`)

Status: `proposed (reconstructed)`. Data do retro: 2026-10-22 (não a data original do stub, que predates ao registro). Decisão original: `engine/vectorized` como stub raso (evidência: `work/test_tdd8_red.py` não salvo no repo; `backtest_core.py` como módulo real com 60 linhas). Decisão reconstruída: aprofundar como módulo profundo, absorvendo `backtest_core`, `monte_carlo`, `deflated_sharpe`; interface única; testes concentrados; adaptadores CSV + MQL5 confirmam seam real.
