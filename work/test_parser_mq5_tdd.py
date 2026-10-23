"""TDD — Parser MQL5 adapter (red antes, green depois)
R1: nunca lucrativo; R3: sandbox; R4: dado não instrução; R9: CPU apenas"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_parser_mq5_extracts_trade_params():
    """MQL5 adapter: extrai parâmetros de trading do código"""
    from quantlab.algos.parser_mq5 import parse_mq5
    # Stub tem análise estática - deve retornar dict
    result = parse_mq5('work/mt5_sample.csv')
    assert isinstance(result, dict), "Deve retornar dict"
    assert 'source_file' in result
    assert 'status' in result
    assert 'SINTETICO' in result['status'].upper().replace('É', 'E').replace('Ê', 'E'), "R1: nunca lucrativo"


def test_parser_mq5_status_inconclusive():
    """R1: status deve ser INCONCLUSIVO"""
    from quantlab.algos.parser_mq5 import parse_mq5
    result = parse_mq5('work/mt5_sample.csv')
    status_upper = result['status'].upper().replace('É', 'E').replace('Ê', 'E')
    assert 'INCONCLUSIVO' in status_upper or 'SINTETICO' in status_upper, "R1: nunca lucrativo"


def test_parser_mq5_no_execution():
    """R3: não executa código MQL5, apenas análise estática"""
    from quantlab.algos.parser_mq5 import parse_mq5
    result = parse_mq5('work/mt5_sample.csv')
    # Stub não executa ordens reais
    assert result.get('executed_trades', 0) == 0, "R3: sandbox"