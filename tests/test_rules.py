def rule(amount): return 0.9 if amount > 50000 else 0.2
def test_high_value_flagged(): assert rule(60000) == 0.9
def test_low_value_ok(): assert rule(500) == 0.2
