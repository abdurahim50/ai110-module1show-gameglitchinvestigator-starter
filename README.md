# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**Game's purpose:** A number guessing game built with Streamlit. You pick a difficulty, guess a number within the range, and use the "higher/lower" hints to find the secret before running out of attempts.

**Bugs found:** (1) the hints were backwards, (2) the difficulty range was inconsistent (Hard said 1–50 but the info box said 1–100 and the secret could be 74), and (3) changing difficulty didn't reset the game so it showed "Game over" before I guessed. See `reflection.md` for the full Bug Reproduction Log.

**Fixes applied:** Refactored the game logic into `logic_utils.py`, corrected the high/low hint wording, generated the secret from the selected difficulty's range, and reset game state whenever the difficulty changes. Verified with `pytest` (4 passing) and by replaying the game.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Open the sidebar and pick a difficulty. The range and attempts allowed update to match (Easy is 1 to 20, Normal is 1 to 100, Hard is 1 to 50).
2. Read the info box. It now shows the correct range for whatever difficulty you picked, plus how many attempts you have left.
3. Type a number into "Enter your guess" and hit Submit Guess. If you guess too high it tells you to go LOWER, and if you guess too low it tells you to go HIGHER — the hints finally point the right way.
4. Keep guessing. The attempts-left counter goes down by one each time, and the secret number stays the same the whole round (you can confirm this in the Developer Debug Info panel).
5. Guess the secret and you win, with balloons and a final score. If you change the difficulty mid-game, it starts a fresh, playable game instead of carrying over a "Game over."

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest tests/ -v
=========================================================== test session starts ============================================================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /home/yongh/code/codepath/ai110-module1show-gameglitchinvestigator-starter/.venv/bin/python
cachedir: .pytest_cache
rootdir: /home/yongh/code/codepath/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.14.0
collected 4 items                                                                                                                          

tests/test_game_logic.py::test_winning_guess PASSED                                                                                  [ 25%]
tests/test_game_logic.py::test_guess_too_high PASSED                                                                                 [ 50%]
tests/test_game_logic.py::test_guess_too_low PASSED                                                                                  [ 75%]
tests/test_game_logic.py::test_hard_difficulty_range PASSED                                                                          [100%]

============================================================ 4 passed in 0.01s =============================================================
```

## 🚀 Stretch Features

### Challenge 4: Enhanced Game UI

- [x] Enhanced UI implemented.

I added two user-friendly enhancements that improve feedback without changing the core game rules:

1. **Hot / Warm / Cold proximity cues.** After each guess, the game shows how close you are with an emoji label (🔥 Hot, ♨️ Warm, ❄️ Cold, or 🎯 Bullseye). The closeness is judged relative to the difficulty's range, so "Hot" feels consistent across Easy/Normal/Hard. This is computed by the new `proximity(guess, secret, low, high)` function in `logic_utils.py` and displayed alongside the higher/lower hint in `app.py` (see the `if submit:` block).

2. **Session summary table.** A "📊 Your guesses this round" table at the bottom lists every guess with its attempt number, the value guessed, the result (Win / Too High / Too Low), and the proximity label. This is rendered with `st.table(st.session_state.history)` near the end of `app.py`, and each row is recorded as a structured dict in the `if submit:` handler.

Both features leave `check_guess`, `parse_guess`, `update_score`, and the win/lose logic untouched — they only add presentation on top.
