import sys, os; sys.path.insert(0, "D:\programação\QUANT_LAB_CLAUDE_")
from work.monte_carlo import monte_carlo
def test_mc_inconclusive(): result = monte_carlo(); assert result["status"].startswith("INCONCLUSIVO"); assert result["label"].startswith("SINTETICO")
