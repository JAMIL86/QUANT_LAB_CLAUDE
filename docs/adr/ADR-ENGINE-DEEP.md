# ADR-ENGINE-DEEP — Deepening do engine (reconstruído, retro)

Status: `implemented` — decisão implementada em 2026-10-23 (commit 5494b2a).
Data do retro: 2026-10-22.
Data original (inferida): anterior ao commit `42c20ce` (Fase 3 PBO).
Data de implementação: 2026-10-23.

## Decisão original (observada no código)

Módulo `engine/vectorized` criado como stub raso (referência: `/tmp/test_tdd8_red.py`, não salvo no repo; `work/test_tdd8_red.py` não existe). A lógica de cálculo foi distribuída em módulos rasos: `work/backtest_core.py` (60 linhas, interface pública `run_backtest`), `work/monte_carlo.py`, `work/deflated_sharpe.py`, `work/walk_forward.py`.

Evidência no gap-register (`docs/retro/gap-register.md`, G-001, P1/M, Strong):
- Thinking: decisão não registrada por escrito (`CONTEXT.md` ausente antes deste retro).
- Coding practice: módulos rasos repetem cálculo; falta `locality`.
- Forward fix: aprofundar `BacktestEngine` (módulo profundo), interface única, absorver módulos rasos.

## Decisão reconstruída (este ADR)

Aprofundar `BacktestEngine` (nome de domínio definido em `CONTEXT.md`) como módulo profundo. Interface pública preservada (`run_backtest`). Implementação absorve `backtest_core`, `monte_carlo`, `deflated_sharpe`. Adaptadores CSV + MQL5 confirmam o seam como real (`codebase-design`: dois adaptadores = real).

## Por que reabrir (não é apenas histórico)

O stub raso não atende os requisitos F0-F4. O gap-register confirma `P1/M` (esforço médio, impacto alto). Sem o registro, futuras revisões arquiteturais (como esta, via `/improve-codebase-architecture`) poderiam sugerir novamente o aprofundamento, sem saber que já foi decidido.

## Confirmação necessária

Este ADR é reconstruído (`proposed`). Confirmação do proprietário do projeto (usuário) necessária para `accepted`. Se rejeitado com razão de carga (ex: "não vale o esforço M para este projeto"), registrar como `wont-fix` com motivo no gap-register.
