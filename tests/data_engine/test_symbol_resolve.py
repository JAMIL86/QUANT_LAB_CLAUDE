"""
Loop de feedback para o bug do feed: 'NoneType' object is not iterable.

Sintoma no dashboard (Symbol Feed, coluna Status):
    ERR: 'NoneType' object is not iterable

Origem: MarketDataCollector._resolve_symbol itera sobre o retorno de
mt5.symbols_get() sem checar None. Quando o terminal não está conectado
(IPC -10004), symbols_get() retorna None e a exceção vaza para o status.
"""

from data_engine.market_data_collector import MarketDataCollector


class _MT5SemConexao:
    """Simula o módulo MT5 quando o terminal não responde (No IPC connection)."""

    def symbols_get(self):
        return None


def test_resolve_symbol_nao_quebra_quando_symbols_get_retorna_none():
    resolved = MarketDataCollector._resolve_symbol(_MT5SemConexao(), "XAUUSD")
    assert resolved is None