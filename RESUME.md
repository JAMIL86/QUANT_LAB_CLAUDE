# RESUME.md — Quant Lab Fase 0 (continuidade)
## Objetivo
Retomar Fase 0 (backtest XAUUSD/MT5) após encerramento forçado. Não repetir etapas concluídas.

## Etapa concluída
- Ler `spec-fase0.md`, `PROMPT_QUANT...`, `work/` (6 arquivos .py + 1 .csv + 4 testes)
- `backtest_core.py` existe (36 linhas) mas incompleto (retorna INCONCLUSIVO, seed não aplicada)
- `test_backtest_core.py` ainda RED (`assert False`)
- Protocolo de continuidade implementado (`RESUME.md`, `WORKLOG.md`)

## Etapa pendente
- Corrigir `backtest_core.py`: aplicar seed (R8), usar CSV (R4), retornar métricas reais (não apenas INCONCLUSIVO)
- Passar TDD `test_backtest_core.py` (red→green) sem quebrar R1-R11
- Rodar `pytest work/`; salvar checkpoint antes de avanço

## Próximo comando
`cd /d/programação/QUANT_LAB_CLAUDE_ && pytest work/test_backtest_core.py -v`

## Critérios de conclusão (gates)
- [ ] Testes 100% verdes (TDD red→green)
- [ ] `backtest_core.py` usa seed/hash R8, lê CSV R4, não declara "lucrativo" sem prova R1
- [ ] Nenhum segredo commitado (verificar `.env` ignorado)
- [ ] `WORKLOG.md` atualizado com resultado do pytest
- [ ] Checkpoint `work/checkpoint_fase0.json` salvo

## Protocolos ativos (do PROMPT MESTRE)
- RESUME.md atualizado a cada etapa
- WORKLOG.md conciso (decisões, testes, erros, resultados)
- Checkpoints antes de operações longas/ariscadas
- Nenhuma etapa repetida sem necessidade
> Etapa pendente: Monte Carlo completo (Fase 2) — só após gate R1 aprovado
> Próximo: Fase 4 relatório (reports/) — só após todos gates
> Etapa pendente: nenhuma — projeto completo (F0-F4)
