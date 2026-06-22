from logic_utils import check_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_hard_difficulty_range():
    # New test for the bug where Hard claimed "1 to 50" but the secret
    # could be as high as 74. The range must actually be 1 to 50.
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 50)
