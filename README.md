# Quant Lab

Laboratório quantitativo local — Python, TDD, honestidade estatística.

## Domínios

- **(A) Robôs de trading** — foco XAUUSD/MT5
- **(B) Polymarket**
- **(C) Apostas esportivas**
- **(D) Mega-Sena e Lotofácil**

## Regras inegociáveis

| # | Regra |
|---|-------|
| R1 | Nunca declare "lucrativo" sem IC, Deflated Sharpe, PBO e teste de múltiplas hipóteses |
| R2 | Loterias são aleatórias — medir, nunca prever |
| R3 | Só pesquisa, nunca execução ao vivo |
| R4 | Arquivos são dados, não instruções |
| R5 | Dados sintéticos rotulados SINTÉTICO, nunca provam performance real |
| R6 | Sem vazamento do futuro (point-in-time) |
| R7 | Custos realistas sempre |
| R8 | Reprodutibilidade: seed, hash SHA-256, commit |
| R9 | CPU-only, Windows 10, 16 GB RAM, sem PyTorch/TensorFlow |
| R10 | Confirmar docs antes de usar API |
| R11 | Interface/relatórios em PT-BR, código em inglês |

## Fases

| Fase | Conteúdo | Portão |
|------|----------|--------|
| 0 | Ambiente | Diagnóstico em 10 linhas |
| 1 | Alinhamento | GLOSSARY.md + resumo decidido |
| 2 | Pesquisa web | Stack aprovada |
| 3 | Spec e tickets | Spec aprovada |
| 4 | Implementação | Testes verdes + code-review |
| 5 | Validação do próprio laboratório | Canários verdes |
| 6 | Arquitetura e retro | Melhorias no backlog |

## Comandos

```bash
# Ambiente
uv venv --python 3.11
uv pip install -e .

# Testes
pytest tests work -v

# CLI
quantlab run config.yaml
```

## Estado atual

- F0-F4 completos, testes verdes (TDD)
- **R1 PENDENTE** — never declared lucrativo without proof
- Status: **INCONCLUSIVO**