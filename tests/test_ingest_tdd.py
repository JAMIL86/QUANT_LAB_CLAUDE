import csv, os
def test_mt5_csv_exists():
    assert os.path.exists("D:\programação\QUANT_LAB_CLAUDE_\work\mt5_sample.csv")
def test_mt5_has_columns():
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "work", "mt5_sample.csv")) as f:
        row = next(csv.DictReader(f))
        assert len(row) > 0
