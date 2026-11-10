# src/quantlab/algos/parser_mq5.py — adapter MQL5 (análise estática)
"""Análise estática de arquivos .mq5 (leitura de código, sem execução — R3/R4).

Este adapter extrai parâmetros de estratégia do código MQL5:
- Funções de trading (OnTick, OnInit, etc)
- Parâmetros de entrada (input)
- Chamadas de funções de trade (OrderSend, etc)
- Níveis de SL/TP
"""
import re
import os


def parse_mq5(path: str) -> dict:
    """Parse MQL5 file and extract strategy parameters.

    Args:
        path: caminho para arquivo .mq5

    Returns:
        dict com parâmetros extraídos (análise estática, sem execução)
    """
    if not os.path.exists(path):
        return {"source_file": path, "error": "arquivo nao encontrado", "status": "INCONCLUSIVO"}

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extrair funções principais
    has_oninit = "OnInit" in content
    has_ontick = "OnTick" in content
    has_oncalc = "OnCalculate" in content
    has_ondeinit = "OnDeinit" in content

    # Contar funções de trade
    trade_functions = len(re.findall(r"OrderSend|Trade\.Position|Position\.", content))

    # Extrair parâmetros de entrada (input)
    input_params = re.findall(r'input\s+(\w+)\s+(\w+)\s*=\s*([^;]+);', content)
    inputs = [{"type": m[0], "name": m[1], "default": m[2].strip()} for m in input_params]

    # Extrair níveis de SL/TP
    sl_patterns = re.findall(r'(?:StopLoss|SL|m_stoploss)\s*[=:]?\s*([0-9.]+)', content, re.IGNORECASE)
    tp_patterns = re.findall(r'(?:TakeProfit|TP|m_takeprofit)\s*[=:]?\s*([0-9.]+)', content, re.IGNORECASE)

    # Detectar tipo de estratégia
    is_martingale = "martingale" in content.lower() or "multiplier" in content.lower()
    is_grid = "grid" in content.lower() or "level" in content.lower()
    is_scalping = len(re.findall(r"OnTick", content)) > 0 and trade_functions > 5

    result = {
        "source_file": path,
        "has_oninit": has_oninit,
        "has_ontick": has_ontick,
        "has_oncalculate": has_oncalc,
        "has_ondeinit": has_ondeinit,
        "trade_functions_count": trade_functions,
        "input_parameters": inputs,
        "sl_levels_found": len(sl_patterns),
        "tp_levels_found": len(tp_patterns),
        "strategy_type": _detect_strategy_type(is_martingale, is_grid, is_scalping, trade_functions),
        "status": "SINTÉTICO — análise estática apenas (R4 sandbox, R1 PENDENTE)",
        "executed_trades": 0,  # R3: nunca executa ordens reais
        "rules_applied": ["R1", "R3", "R4", "R9"]
    }

    return result


def _detect_strategy_type(is_martingale: bool, is_grid: bool, is_scalping: bool, trade_count: int) -> str:
    """Detecta o tipo de estratégia baseado nos padrões encontrados."""
    if is_martingale:
        return "MARTINGALE"
    if is_grid:
        return "GRID"
    if is_scalping:
        return "SCALPING"
    if trade_count > 0:
        return "SWING"
    return "UNKNOWN"


def get_strategy_summary(path: str) -> str:
    """Retorna resumo textual da estratégia (para logs/debug)."""
    result = parse_mq5(path)
    summary = f"Arquivo: {result['source_file']}\n"
    summary += f"Tipo: {result.get('strategy_type', 'UNKNOWN')}\n"
    summary += f"Funções de trade: {result.get('trade_functions_count', 0)}\n"
    summary += f"Parâmetros de entrada: {len(result.get('input_parameters', []))}\n"
    summary += f"Status: {result['status']}"
    return summary


__all__ = ["parse_mq5", "get_strategy_summary"]