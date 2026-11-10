import sys, os
sys.path.insert(0, 'D:\programação\QUANT_LAB_CLAUDE_')
from work.deflated_sharpe import deflated_sharpe

def test_deflated_sharpe_inconclusive():
    result = deflated_sharpe(1.5, trials=10)
    assert result['status'].startswith('INCONCLUSIVO'), "Ticket 3: R1 respeitado — nao declara lucrativo"
    assert result['label'].startswith('SINTETICO'), "Ticket 3: R5 — sintetico marcado"
    assert 'deflated_sharpe' in result
