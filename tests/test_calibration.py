from epifair.uncertainty.calibration import expected_calibration_error,brier_score

def test_perfect_calibration_simple():
    assert expected_calibration_error([1,0],[1,0],n_bins=2)==0
    assert brier_score([1,0],[1,0])==0
